from flask import Flask, request
import time
import csv
import sys
import json
import requests
import os
import random
import string

SYSTEM_MANAGER_URL = "0.0.0.0:10000"
NUMBER_OF_SERVERS = os.environ.get("TEST2_SERVERS", 1)

deployment_descriptor = {}
with open('client-server.json') as json_file:
    deployment_descriptor = json.load(json_file)

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
            time.sleep(30)

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
            if app.get("application_name") == "nettime":
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


def scale_up_service(amount, microserviceid):
    print("\t Asking scaleup of n.", amount, " insances of ", microserviceid)
    token = getlogin()
    for i in range(int(amount)):
        url = "http://" + SYSTEM_MANAGER_URL + "/api/service/" + microserviceid + "/instance"
        resp = requests.post(url, headers={'Authorization': 'Bearer {}'.format(token)})
        time.sleep(1)
    pass



if __name__ == '__main__':
    print("Test 2 - Net Time")

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

    print("Scaling up the Servers")
    scale_up_service(NUMBER_OF_SERVERS, microservices[1])

    print("Deployment of the client")
    scale_up_service(1, microservices[0])

    print("Waiting for 60 seconds cooldown")
    time.sleep(60)

    print("Check deployment status")
    succeeded, returntext = check_deployment(microservices)
    attempt = 1
    while not succeeded:
        if attempt > 3:
            print("Deployment failed with error: ", returntext)
            print("Forcing undeployment. Please wait for the cleanup to finish")
            delete_all_apps()
            time.sleep(60)
            print("You may now fix your infrastructure and re-try the test")
            exit(1)
        attempt += 1
        print("Deployment not finished yet")
        time.sleep(60)
        succeeded, returntext = check_deployment(microservices)

    print("The cluster is working")
    print("Executing the benchmark... this might take up to 20/30 seconds")
    url = "http://" + returntext + ":50002/10.30.30.30/oakestra/results.csv"
    r = requests.get(url, timeout=200)

    if r.status_code != 200:
        print("benchmark failed. Check if oakestra network is configured correctly and the worker node is reachable.")
        print("Forcing undeployment. Please wait for the cleanup to finish")
        undeploy_all(appid)
        time.sleep(20)
        print("You may now fix your infrastructure and re-try the test")
        exit(1)

    print("Benchmark succeeded! Results: ")
    print("removing the application")
    undeploy_all(appid)
    print("printing results:")
    print(r.text)
