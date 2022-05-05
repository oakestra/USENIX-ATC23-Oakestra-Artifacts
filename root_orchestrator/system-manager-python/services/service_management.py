import logging

from ext_requests.apps_db import mongo_find_job_by_id, mongo_insert_job, mongo_get_applications_of_user, \
    mongo_delete_job, mongo_find_app_by_id, mongo_get_jobs_of_application, mongo_get_all_jobs
from services.application_management import get_user_app, update_app, add_service_to_app, remove_service_from_app
from services.instance_management import scale_down_instance
from sla.versioned_sla_parser import parse_sla_json
from flask_smorest import abort


def create_services_of_app(username, sla, force=False):
    data = parse_sla_json(sla)
    logging.log(logging.INFO, sla)
    app_id = data.get('applications')[0]["applicationID"]
    last_service_id = ""
    if mongo_find_app_by_id(app_id, username) is None:
        abort(404, {"message": "app not found"})
    for microservice in data.get('applications')[0].get('microservices'):
        # Insert job into database
        last_service_id = mongo_insert_job(
            {
                'file_content': generate_db_structure(data.get('applications')[0], microservice)
            })
        # Insert job into app's services list
        add_service_to_app(app_id, last_service_id, username)
        # TODO: check if service deployed already etc. force=True must force the insertion anyway
    return {'job_id': str(last_service_id)}


def delete_service(username, serviceid):
    apps = mongo_get_applications_of_user(username)
    for application in apps:
        if serviceid in application["microservices"]:
            # undeploy instances
            scale_down_instance(serviceid, username)
            # remove service from app's services list
            remove_service_from_app(application["applicationID"], serviceid, username)
            # remove service from DB
            mongo_delete_job(serviceid)
            return True
    return False


def update_service(username, sla, serviceid):
    create_services_of_app(username, sla, force=True)


def user_services(appid, username):
    application = mongo_find_app_by_id(appid, username)
    if application is None:
        abort(404, {"message": "app not found"})

    return mongo_get_jobs_of_application(appid)


def get_service(serviceid, username):
    apps = mongo_get_applications_of_user(username)
    for application in apps:
        if serviceid in application["microservices"]:
            return mongo_find_job_by_id(serviceid)


def get_all_services():
    return mongo_get_all_jobs()


def generate_db_structure(application, microservice):
    microservice["applicationID"] = application["applicationID"]
    microservice["app_name"] = application["application_name"]
    microservice["app_ns"] = application["application_namespace"]
    microservice["image"] = microservice["code"]
    addresses = microservice.get("addresses")
    if addresses is not None:
        microservice["RR_ip"] = addresses.get("rr_ip")  # compatibility with older netmanager versions
    return microservice
