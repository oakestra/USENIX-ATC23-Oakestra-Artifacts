import os
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import json
from datetime import datetime

MONGO_URL  = os.environ.get('CLUSTER_MONGO_URL')
MONGO_PORT = os.environ.get('CLUSTER_MONGO_PORT')

MONGO_ADDR_NODES = 'mongodb://' + str(MONGO_URL) + ':' + str(MONGO_PORT) + '/nodes'
MONGO_ADDR_JOBS = 'mongodb://' + str(MONGO_URL) + ':' + str(MONGO_PORT) + '/jobs'


mongo_nodes = None
mongo_jobs = None
app = None


def mongo_init(flask_app):
    global app
    global mongo_nodes, mongo_jobs

    app = flask_app

    mongo_nodes = PyMongo(app, uri=MONGO_ADDR_NODES)
    mongo_jobs = PyMongo(app, uri=MONGO_ADDR_JOBS)

    app.logger.info("MONGODB - init mongo")


# ................. Worker Node Operations ...............#
###########################################################

def mongo_upsert_node(obj):
    global app, mongo_nodes
    app.logger.info("MONGODB - upserting node...")
    json_node_info = json.loads(obj['node_info'])
    node_info_hostname = json_node_info.get('host')

    nodes = mongo_nodes.db.nodes
    # find node by hostname and if it exists, just upsert
    node_id = nodes.find_one_and_update({'node_info.host': node_info_hostname},
                                        {'$set': {'node_info': json_node_info}},
                                        upsert=True, return_document=True).get('_id')
    app.logger.info(node_id)
    return node_id


def mongo_find_node_by_id(node_id):
    global mongo_nodes
    return mongo_nodes.db.nodes.find_one(node_id)


def mongo_find_node_by_name(node_name):
    global mongo_nodes
    try:
        return mongo_nodes.db.nodes.find_one({'node_info.host': node_name})
    except Exception as e:
        return 'Error'


def mongo_find_node_by_id_and_update_cpu_mem(node_id, node_cpu_used, cpu_cores_free, node_mem_used, node_memory_free_in_MB):
    global app, mongo_nodes
    app.logger.info('MONGODB - update cpu and memory of worker node {0} ...'.format(node_id))
    # o = mongo.db.nodes.find_one({'_id': node_id})
    # print(o)

    time_now = datetime.now()

    mongo_nodes.db.nodes.find_one_and_update(
        {'_id': ObjectId(node_id)},
        {'$set': {'current_cpu_percent': node_cpu_used, 'current_cpu_cores_free': cpu_cores_free,
                  'current_memory_percent': node_mem_used, 'current_free_memory_in_MB': node_memory_free_in_MB,
                  'last_modified': time_now, 'last_modified_timestamp': datetime.timestamp(time_now)}},
        upsert=True)

    return 1


def find_one_edge_node():
    """Find first occurrence of edge nodes"""
    global mongo_nodes
    return mongo_nodes.db.nodes.find_one()


def find_all_nodes():
    global mongo_nodes
    return mongo_nodes.db.nodes.find()


def mongo_dead_nodes():
    print('looking for dead nodes')


def mongo_aggregate_node_information(TIME_INTERVAL):
    """ 1. Find all nodes"""
    """ 2. Aggregate cpu, memory, and more information of worker nodes"""

    global mongo_nodes

    cumulative_cpu = 0
    cumulative_cpu_cores = 0
    cumulative_memory = 0
    cumulative_memory_in_mb = 0
    number_of_active_nodes = 0
    technology = []

    nodes = find_all_nodes()
    for n in nodes:
        # print(n)

        # if it is not older than TIME_INTERVAL
        if n.get('last_modified_timestamp') >= (datetime.now().timestamp() - TIME_INTERVAL):
            cumulative_cpu += n.get('current_cpu_percent')
            cumulative_cpu_cores += n.get('current_cpu_cores_free')
            cumulative_memory += n.get('current_memory_percent')
            cumulative_memory_in_mb += n.get('current_free_memory_in_MB')
            number_of_active_nodes += 1
            for t in n.get('node_info').get('technology'):
               technology.append(t) if t not in technology else technology

        else:
            print('Node {0} is inactive.'.format(n.get('_id')))

    jobs = mongo_find_all_jobs()
    for j in jobs:
        print(j)

    return {'cpu_percent': cumulative_cpu, 'memory_percent': cumulative_memory,
            'cpu_cores': cumulative_cpu_cores, 'cumulative_memory_in_mb': cumulative_memory_in_mb,
            'number_of_nodes': number_of_active_nodes, 'jobs': jobs, 'technology': technology, 'more': 0}


# ................. Job Operations .......................#
###########################################################

def mongo_upsert_job(job):
    print('insert/upsert requested job')
    return mongo_jobs.db.jobs.find_one_and_update(job, {'$set': job}, upsert=True, return_document=True)  # if job does not exist, insert it


def mongo_find_job_by_system_id(system_job_id):
    print('Find job by Id and return cluster.. and delete it...')
    # return just the assigned node of the job
    job_obj = mongo_jobs.db.jobs.find_one({'system_job_id': system_job_id})
    return job_obj


def mongo_find_all_jobs():
    global mongo_jobs
    # list (= going into RAM) okey for small result sets (not clean for large data sets!)
    return list(mongo_jobs.db.jobs.find({}, {'_id': 0, 'system_job_id': 1, 'status': 1}))


def mongo_update_job_status(job_id, status):
    global mongo_jobs
    mongo_jobs.db.jobs.find_one_and_update({'_id': ObjectId(job_id)}, {'$set': {'status': status}})