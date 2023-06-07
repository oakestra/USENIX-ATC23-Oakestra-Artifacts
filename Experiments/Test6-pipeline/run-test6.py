from flask import Flask, request
import time
import csv
import sys
import json
import requests
import os
import random
import socket
import subprocess
import signal

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

SYSTEM_MANAGER_URL = "0.0.0.0:10000"
SLA_FILE = os.getenv('TEST7_SLA_FILE', 'pipeline.json')
SERVER_ADDRESS = os.getenv('SERVER_ADDRESS', '192.168.0.2')

deployment_descriptor = {}
with open(SLA_FILE) as json_file:
    deployment_descriptor = json.load(json_file)
    deployment_descriptor["applications"][0]["microservices"][0]["cmd"]+=["--evaluation-address", "http://"+SERVER_ADDRESS+":8000"]
    deployment_descriptor["applications"][0]["microservices"][1]["cmd"]+=["--evaluation-address", "http://"+SERVER_ADDRESS+":8000"]
    deployment_descriptor["applications"][0]["microservices"][2]["cmd"]+=["--evaluation-address", "http://"+SERVER_ADDRESS+":8000"]

app = Flask(__name__)
start = None
stop = None
platform = "oakestra"
testn = 1
ATTEMPT = 10
result = ""
waiting_for_result = True

metrics_process = None
results = []
results.append(["test_n", "platform", "time"])


def get_random_string(length):
    # choose from all lowercase letter
    result_str = ''.join(random.choice('qwertyuiopasdfghjklzxcvbnm') for i in range(length))
    return result_str


def getlogin():
    url = "http://" + SYSTEM_MANAGER_URL + "/api/auth/login"
    credentials = {
        "username": "Admin",
        "password": "Admin"
    }
    r = requests.post(url, json=credentials)
    return r.json()["token"]


def register_app():
    token = getlogin()

    # print(deployment_descriptor)
    head = {'Authorization': "Bearer " + token}
    url = "http://" + SYSTEM_MANAGER_URL + "/api/application"
    deployment_descriptor["applications"][0]["application_namespace"] = get_random_string(5)
    resp = requests.post(url, headers=head, json=deployment_descriptor)

    if resp.status_code == 200:
        json_resp = json.loads(resp.json())
        print(json_resp)
        for app in json_resp:
            if app.get("application_name") == "pipeline":
                json_resp = app
                return json_resp.get("applicationID"), json_resp.get("microservices")
    print(resp)
    return "", []


def check_deployment(microservices):
    token = getlogin()
    head = {'Authorization': 'Bearer {}'.format(token)}
    clientip = "0.0.0.0"
    for microservice in microservices:
        url = "http://" + SYSTEM_MANAGER_URL + "/api/service/" + microservice
        resp = requests.get(url, headers={'Authorization': 'Bearer {}'.format(token)})
        if resp.status_code == 200:
            json_resp = json.loads(resp.json())
            instances = json_resp["instance_list"]
            if instances is not None:
                for instance in instances:
                    try:
                        if json_resp["microservice_name"] == "client":
                            clientip = instance["publicip"]
                        if instance["status"] != "RUNNING":
                            return False, str(json_resp["microservice_name"])
                    except:
                        return False, str(json_resp["microservice_name"])
            else:
                return False, "No instances"
    return True, clientip


def undeploy_all(app_id):
    print("\t Asking Undeployment")
    token = getlogin()
    url = "http://" + SYSTEM_MANAGER_URL + "/api/application/" + str(app_id)
    resp = requests.delete(url, headers={'Authorization': 'Bearer {}'.format(token)})
    time.sleep(10)
    pass


def print_csv():
    with open("results-scheduler.csv", "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(results)

def scale_up_service(amount, microserviceid):
    print("\t Asking scaleup of n.", amount, " insances of ", microserviceid)
    token = getlogin()
    for i in range(int(amount)):
        url = "http://" + SYSTEM_MANAGER_URL + "/api/service/" + microserviceid + "/instance"
        resp = requests.post(url, headers={'Authorization': 'Bearer {}'.format(token)})
        time.sleep(1)
    pass

def delete_all_apps():
    token = getlogin()
    url = "http://" + SYSTEM_MANAGER_URL + "/api/services"
    resp = requests.get(url, headers={'Authorization': 'Bearer {}'.format(token)})
    if resp.status_code == 200:
        json_resp = json.loads(resp.json())
        print(json_resp)
        for app in json_resp:
            url = "http://" + SYSTEM_MANAGER_URL + "/api/application/" + app.get("applicationID")
            r = requests.delete(url, headers={'Authorization': 'Bearer {}'.format(token)})
            print(r)
            print("Waiting undeployment cooldown")
            time.sleep(30)

def call_start_benchmark():
    url = "http://0.0.0.0:8000/start-benchmark"
    r = requests.post(url)
    if r.status_code != 200:
        print("Impossible to call start benchmark. Is it running?")
        exit(1)


def call_start_run():
    url = "http://0.0.0.0:8000/start-run"
    r = requests.post(url, json={})
    if r.status_code != 200:
        print("Impossible to call run benchmark. Is it running?")
        exit(1)


def call_end_run():
    url = "http://0.0.0.0:8000/end-run"
    r = requests.post(url)


def call_end_benchmark():
    url = "http://0.0.0.0:8000/end-benchmark"
    r = requests.post(url)


def signal_handler(sig, frame):
    print('Cleanup process started')
    delete_all_apps()
    if metrics_process is None:
        metrics_process.kill()
    print('Cleanup completed!')
    sys.exit(0)

if __name__ == '__main__':
    print("Test 1 - Deployment Time")
    signal.signal(signal.SIGINT, signal_handler)
    p = subprocess.Popen("./metrics serve",shell=True)
    metrics_process = p

    print("Performing initial cleanup")
    delete_all_apps()
    time.sleep(5)

    print("Registration of the Client-Server Application")
    appid, microservices = register_app()
    if appid == "":
        print("App registration failed")
        print("Forcing undeployment. Please wait for the cleanup to finish")
        undeploy_all(appid)
        time.sleep(20)
        print("You may now fix your infrastructure and re-try the test")
        exit(1)

    print("Initalizing the metrics utility")
    call_start_benchmark()
    call_start_run()

    print("Deployment of the pipeline")
    scale_up_service(1, microservices[3])
    scale_up_service(1, microservices[2])
    scale_up_service(1, microservices[1])
    scale_up_service(1, microservices[0])

    print("Wait for 5 minutes for the benchmark")
    time.sleep(60*5)

    print("Stopping metrics system")
    call_end_run()
    call_end_benchmark()

    print("Benchmark finished, waiting for the cooldown")
    delete_all_apps()

    print("Benchmark finished. Check the results in results/*.csv")
    print("You can now pres Ctrl+C to exit")
    p.kill()
    signal.pause()


