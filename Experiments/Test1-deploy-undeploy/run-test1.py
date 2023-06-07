from flask import Flask, request
import time
import csv
import sys
import json
import requests
import os
import random
import socket

hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)

SYSTEM_MANAGER_URL = "0.0.0.0:10000"
CLIENT_SERVICE_ID = ""
SLA_FILE = os.getenv('TEST1_SLA_FILE', 'client-scheduler.json')
SERVER_ADDRESS = os.getenv('SERVER_ADDRESS', '10.19.1.254')

deployment_descriptor = {}
with open(SLA_FILE) as json_file:
    deployment_descriptor = json.load(json_file)
    deployment_descriptor["applications"][0]["microservices"][0]["environment"]=["SERVER_ADDRESS="+str(SERVER_ADDRESS)+":5001"]

app = Flask(__name__)
start = None
stop = None
platform = "oakestra"
testn = 1
ATTEMPT = 10
result = ""
waiting_for_result = True

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
            if app.get("application_name") == "clientsrvr":
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


@app.route("/")
def index():
    global stop
    global testn
    global waiting_for_result
    if waiting_for_result:
        waiting_for_result = False
        print("Attempt:", testn, "- Received deployment complete webhook")
        stop = time.time()
        data_point = [testn, platform, stop - start]
        results.append(data_point)
        testn += 1
        if testn >= ATTEMPT:
            print_csv()
            delete_all_apps()
            print("Test Finished!!! Ctrl+C to exit")
            exit(0)
        print("Undeployment...")
        undeploy()
        print("Cooldown...")
        time.sleep(15)
        print("Sending again deployment command")
        deploy()
        waiting_for_result = True
    return "", 200


def undeploy():
    print_csv()
    token = getlogin()
    url = "http://" + SYSTEM_MANAGER_URL + "/api/service/" + CLIENT_SERVICE_ID
    resp = requests.get(url, headers={'Authorization': 'Bearer {}'.format(token)})
    if resp.status_code == 200:
        json_resp = json.loads(resp.json())
        instances = json_resp["instance_list"]
        if instances is not None:
            for instance in instances:
                url = "http://" + SYSTEM_MANAGER_URL + "/api/service/" + CLIENT_SERVICE_ID + "/instance/" + str(
                    instance["instance_number"])
                requests.delete(url, headers={'Authorization': 'Bearer {}'.format(token)})
        else:
            return False, "No instances"


def deploy():
    global start
    global result
    token = getlogin()
    url = "http://" + SYSTEM_MANAGER_URL + "/api/service/" + CLIENT_SERVICE_ID + "/instance"
    start = time.time()
    resp = requests.post(url, headers={'Authorization': 'Bearer {}'.format(token)})
    if resp.status_code != 200:
        print("Deploy request failed!!")
        print(resp)
        exit(1)


def print_csv():
    with open("results-scheduler.csv", "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(results)


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

if __name__ == '__main__':
    print("Test 1 - Deployment Time")

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
    CLIENT_SERVICE_ID = microservices[0]
    deploy()
    app.run(host="0.0.0.0", port=5001)
