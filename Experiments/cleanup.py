from flask import Flask, request
import time
import csv
import sys
import json
import requests
import os

SYSTEM_MANAGER_URL = "0.0.0.0:10000"
CLIENT_SERVICE_ID = os.getenv('TEST1_MICROSERVICE_ID')


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


if __name__ == '__main__':
    print("Removing apps")
    delete_all_apps()
    print("Success")