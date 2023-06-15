![Oakestra](res/oakestra-white.png)

[![](https://img.shields.io/badge/USENIX%20ATC%20'23-paper-limegreen)](https://www.oakestra.io/pubs/Oakestra-ATC2023.pdf)
[![](https://img.shields.io/badge/wiki-website-blue)](https://www.oakestra.io/docs/)
[![](https://img.shields.io/badge/Discord-%235865F2.svg?&logo=discord&logoColor=white)](https://discord.gg/7F8EhYCJDf)



# Oakestra USENIX ATC 2023 Artifacts 
## Orchestrator Repository

This repository contains the artifacts for the paper:

### Oakestra: A Lightweight Hierarchical Orchestration Framework for Edge Computing

> **Abstract:** Edge computing seeks to enable applications with strict latency requirements by utilizing resources deployed in diverse, dynamic, and possibly constrained environments closer to the users. Existing state-of-the-art orchestration frameworks(e.g. Kubernetes) perform poorly at the edge since they were designed for reliable, low latency, high bandwidth cloud environments. We present Oakestra, a hierarchical, lightweight, flexible, and scalable orchestration framework for edge computing. Through its novel federated three-tier resource management, delegated task scheduling, and semantic overlay networking, Oakestra can flexibly consolidate multiple infrastructure providers and support applications over dynamic variations at the edge. Our comprehensive evaluation against the state-of-the-art demonstrates the significant benefits of Oakestra as it achieves an approximately tenfold reduction in resource usage through reduced management overhead and 10% application performance improvement due to lightweight operation over constrained hardware.

[Oakestra](https://oakestra.io) is an open-source project. Most of the code used for this paper is upstream, or is in the process of being upstreamed.

```
@inproceedings {Bartolomeo2023,
author = {Bartolomeo, Giovanni and Yosofie, Mehdi and Bäurle, Simon and Haluszczynski, Oliver and Mohan, Nitinder and Ott, Jörg},
title = {{Oakestra}: A Lightweight Hierarchical Orchestration Framework for Edge Computing},
booktitle = {2023 USENIX Annual Technical Conference (USENIX ATC 23)},
year = {2023},
address = {Boston, MA},
url = {https://www.usenix.org/conference/atc23/presentation/bartolomeo},
publisher = {USENIX Association},
month = jul,
}
```

## Artifact Structure

There are a total of three artifact repositories for reproducing the experiments and results in the paper. 

1. [**This**] [Orchetrator repository](https://github.com/oakestra/USENIX-ATC23-Oakestra-Artifacts/tree/main/Experiments): The  repository contains the Root & Cluster orchestrators   folders, as well as the Node Engine source code for the worker node.

2. [Network repository](https://github.com/oakestra/USENIX-ATC23-Oakestra-net-Artifacts): This repository contains the  Root, Cluster, and Worker network components.

3. [Experiments repository](https://github.com/oakestra/USENIX-ATC23-Oakestra-Artifacts/tree/main/Experiments): This repository includes the setup instructions to create your first Oakestra infrastructure and a set of scripts to automate the results collection procedure and reproducing our results.

4. [_Optional_] [Dashboard](https://github.com/oakestra/dashboard): The repository contains a front-end application that can be used to graphically interact with the platform. Its optional but gives a nice web-based GUI to Oakestra

### Q. I want to recreate the experiments in the paper. What should I do?

A. We have created a detailed `README` and `getting-started` guide that provides step-by-step instructions which you can find [here](https://github.com/oakestra/USENIX-ATC23-Oakestra-Artifacts/blob/main/Experiments/README.pdf).

> The rest of the repository will detail how to set up the Oakestra orchestrators. You can just follow these steps or take a look at our README file for instructions.

### Q. I just want to try out Oakestra. Should I continue with this repo?

A. This repository is recreating our USENIX ATC artifacts and is, therefore, out-of-sync of the main Oakestra development. Please see the `main` [Oakestra](https://github.com/oakestra/oakestra) for the latest features.

---


## What is inside this repository?

`system-manager-python/` and `cloud_scheduler/` contain the  `System Manager` and the `Cloud Scheduler` source code, respectively. Similarly, inside the `Cluster Orchestrator` folder, we find the source of the `cluster-manager/` and the `cluster-scheduler/`. Finally, the `go-node-engine/` contains the implementation of the `Node Engine`. The root and cluster components are implemented using `Python`, while the Node Engine is implemented in `Go` for easy integration with the runtime environments and better performance. 

Both cluster and root contain a `docker-compose` file for simplifying the build and run process. 

## Set up your cluster

We will first create a development cluster in your infrastructure.

### Deploy a Root Orchestrator 

On a Linux machine with public IP address or DNS name, first install Docker and Docker-compose. Then, run the following commands to set up the Root Orchestrator components. 

```bash
cd root_orchestrator/
docker-compose up --build 
```

The following ports are exposed:

- Port 80 - Grafana Dashboard (It can be used to monitor the clsuter status)
- Port 10000 - System Manager (It needs to be accessible from the Cluster Orchestrator)


### Deploy one or more Cluster Orchestrator(s)

For each one of the cluster orchestrator that needs to be deployed 

- Log into a Linux machine with public IP address or DNS name
- Install Docker and Docker-compose.
- Export the required parameters:

```
export SYSTEM_MANAGER_URL=" < ip address of the root orchestrator > "
export CLUSTER_NAME=" < name of the cluster > "
export CLUSTER_LOCATION=" < location of the cluster > "
```

- Then, run the following commands to set up the Cluster Orchestrator components. 

```bash
cd cluster_orchestrator/
docker-compose up --build 
```

The following ports are exposed:

- 10100 Cluster Manager (needs to be accessible by the Node Engine)

### Add worker nodes (run Node Engine)

*Requirements*
- Linux OS with the following packages installed (Ubuntu and many other distributions natively supports them)
  - iptable
  - ip utils
- port 50103 available

1) First you need to install the go Node Engine.
```
wget -c https://github.com/oakestra/oakestra/releases/download/v0.4.2/NodeEngine_$(dpkg --print-architecture).tar.gz && tar -xzf NodeEngine_$(dpkg --print-architecture).tar.gz && chmod +x install.sh && ./install.sh
```
2) (Optional, required only if you want to enable communication across the microservices) Install the [OakestraNet/Node_net_manager](https://github.com/oakestra/oakestra-net/tree/main/node-net-manager) component using the following commsnd:
```
wget -c https://github.com/oakestra/oakestra-net/releases/download/v0.4.2/NetManager_$(dpkg --print-architecture).tar.gz && tar -xzf NetManager_$(dpkg --print-architecture).tar.gz && chmod +x install.sh && ./install.sh $(dpkg --print-architecture)
```
2.1) Configure the NetManager config file accordingly to what stated in the [NetManager Readme](https://github.com/oakestra/oakestra-net/blob/main/node-net-manager/README.md). Leave the ClusterMqttPort value to the default 10003 value.  
2.2) Run the NetManager using `sudo NetManager -p 6000`
3) Run the node engine: `sudo NodeEngine -a <cluster orchestrator address> -p <cluster orhcestrator port e.g. 10100> -n 6000`. If you specifcy the flag `-n 6000`, the NodeEngine expects a running NetManager component on port 6000. If this is the case, the node will start in overlay mode, enabling the networking across the deployed application. In order to do so, you need to have the Oakestra NetManager component installed on your worker node ([OakestraNet/Node_net_manager](https://github.com/oakestra/oakestra-net/tree/main/node-net-manager)). If you don't which to enable the networking, simply avoid specifying the flag -n. Use NodeEngine -h for further details
3.1) As an alternative you can run the development version of the NodeEngine moving inside `go_node_engine` and running `sudo go NodeEngine -a <cluster orchestrator address> -p <cluster orhcestrator port e.g. 10100> -n <net manager port>`

## Use the APIs to deploy a new application

### Deployment descriptor

In order to deploy a container a deployment descriptor must be passed to the deployment command. 
The deployment descriptor contains all the information that Oakestra needs in order to achieve a complete
deploy in the system. 

Since version 0.4, Oakestra (previously, EdgeIO) uses the following deployment descriptor format. 

`deploy_curl_application.yaml`

```yaml
{
  "sla_version" : "v2.0",
  "customerID" : "Admin",
  "applications" : [
    {
      "applicationID" : "",
      "application_name" : "clientsrvr",
      "application_namespace" : "test",
      "application_desc" : "Simple demo with curl client and Nginx server",
      "microservices" : [
        {
          "microserviceID": "",
          "microservice_name": "curl",
          "microservice_namespace": "test",
          "virtualization": "container",
          "cmd": ["sh", "-c", "tail -f /dev/null"],
          "memory": 100,
          "vcpus": 1,
          "vgpus": 0,
          "vtpus": 0,
          "bandwidth_in": 0,
          "bandwidth_out": 0,
          "storage": 0,
          "code": "docker.io/curlimages/curl:7.82.0",
          "state": "",
          "port": "9080",
          "added_files": []
        },
        {
          "microserviceID": "",
          "microservice_name": "nginx",
          "microservice_namespace": "test",
          "virtualization": "container",
          "cmd": [],
          "memory": 100,
          "vcpus": 1,
          "vgpus": 0,
          "vtpus": 0,
          "bandwidth_in": 0,
          "bandwidth_out": 0,
          "storage": 0,
          "code": "docker.io/library/nginx:latest",
          "state": "",
          "port": "6080:60/tcp",
          "addresses": {
            "rr_ip": "10.30.30.30"
          },
          "added_files": []
        }
      ]
    }
  ]
}
```

This deployment descriptor example generates one application named *clientserver* with the `test` namespace and two microservices:
- nginx server with test namespace, namely `clientserver.test.nginx.test`
- curl client with test namespace, namely `clientserver.test.curl.test`

This is a detailed description of the deployment descriptor fields currently implemented:
- sla_version: the current version is v0.2
- customerID: id of the user, default is Admin
  - application list, in a single deployment descriptor is possible to define multiple applications, each containing:
    - Fully qualified app name: A fully qualified name in Oakestra is composed of 
        - application_name: unique name representing the application (max 10 char, no symbols)
        - application_namespace: namespace of the app, used to reference different deployment of the same application. Examples of namespace name can be `default` or `production` or `test` (max 10 char, no symbols)
        - applicationID: leave it empty for new deployments, this is needed only to edit an existing deployment.  
    - application_desc: Short description of the application
    - microservice list, a list of the microservices composing the application. For each microservice the user can specify:
      - microserviceID: leave it empty for new deployments, this is needed only to edit an existing deployment.
      - Fully qualified service name:
        - microservice_name: name of the service (max 10 char, no symbols)
        - microservice_namespace: namespace of the service, used to reference different deployment of the same service. Examples of namespace name can be `default` or `production` or `test` (max 10 char, no symbols)
      - virtualization: currently the only uspported virtualization is `container`
      - cmd: list of the commands to be executed inside the container at startup
      - vcpu,vgpu,memory: minimum cpu/gpu vcores and memory amount needed to run the container
      - vtpus: currently not implemented
      - storage: minimum storage size required (currently the scheduler does not take this value into account)
      - bandwidth_in/out: minimum required bandwith on the worker node. (currently the scheduler does not take this value into account)
      - port: port mapping for the container in the syntax hostport_1:containerport_1\[/protocol];hostport_2:containerport_2\[/protocol] (default protocol is tcp)
      - addresses: allows to specify a custom ip address to be used to balance the traffic across all the service instances. 
        - rr\_ip: [optional filed] This field allows you to setup a custom Round Robin network address to reference all the instances belonging to this service. This address is going to be permanently bounded to the service. The address MUST be in the form `10.30.x.y` and must not collide with any other Instance Address or Service IP in the system, otherwise an error will be returned. If you don't specify a RR_ip and you don't set this field, a new address will be generated by the system.
      - constraints: array of constraints regarding the service. 
        - type: constraint type
          - `direct`: Send a deployment to a specific cluster and a specific list of eligible nodes. You can specify `"node":"node1;node2;...;noden"` a list of node's hostnames. These are the only eligible worker nodes.  `"cluster":"cluster_name"` The name of the cluster where this service must be scheduled. E.g.:
         
    ```
    "constraints":[
                {
                  "type":"direct",
                  "node":"xavier1",
                  "cluster":"gpu"
                }
              ]
    ```
 
### Login
After running a cluster you can use the debug OpenAPI page to interact with the apis and use the infrastructure

connect to `<root_orch_ip>:10000/api/docs`

Authenticate using the following procedure:

1. locate the login method and use the try-out button
![try-login](res/login-try.png)
2. Use the default Admin credentials to login
![execute-login](res/login-execute.png)
3. Copy the result login token
![token-login](res/login-token-copy.png)
4. Go to the top of the page and authenticate with this token
![auth-login](res/authorize.png)
![auth2-login](res/authorize-2.png)

### Register an application and the services
After you authenticate with the login function, you can try out to deploy the first application. 

1. Upload the deployment description to the system. You can try using the deployment descriptor above.
![post app](res/post-app.png)

The response contains the Application id and the id for all the application's services. Now the application and the services are registered to the platform. It's time to deploy the service instances! 

You can always remove or create a new service for the application using the /api/services endpoints

### Deploy an instance of a registered service 

1. Trigger a deployment of a service's instance using `POST /api/service/{serviceid}/instance`

each call to this endpoint generates a new instance of the service

### Monitor the service status

1. With `GET /api/aplications/<userid>` (or/api/aplications/ if you're admin) you can check the list of the deployed application.
2. With `GET /api/services/<appid>` you can check the services attached to an application
3. With `GET /api/service/<serviceid>` you can check the status for all the instances of <serviceid>

### Undeploy 

- Use `DELETE /api/service/<serviceid>` to delete all the instances of a service
- Use `DELETE /api/service/<serviceid>/instance/<instance number>` to delete a specific instance of a service
- Use `DELETE /api/application/<appid>` to delete all together an application with all the services and instances

## Networking 

Please see [Oakestra Net Artficat Repository](https://github.com/oakestra/USENIX-ATC23-Oakestra-net-Artifacts) for setting up networking.

## Frontend?

To make your life easier you can run the Oakestra front-end.
Please check the [Dashboard](https://github.com/oakestra/dashboard) repository for more information.

# Beyond the paper


