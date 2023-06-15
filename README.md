![Oakestra](https://github.com/oakestra/oakestra/raw/develop/res/oakestra-white.png)

[![](https://img.shields.io/badge/USENIX%20ATC%20'23-paper-limegreen)](https://www.oakestra.io/pubs/Oakestra-ATC2023.pdf)
[![](https://img.shields.io/badge/wiki-website-blue)](https://www.oakestra.io/docs/)
[![](https://img.shields.io/badge/Discord-%235865F2.svg?&logo=discord&logoColor=white)](https://discord.gg/7F8EhYCJDf)


<img width="40%" src="https://raw.githubusercontent.com/oakestra/oakestra.github.io/69dc5022f80ec4e9b90254ce69b12f05aa5f9d0d/pubs/badges/badges.png" align="right" />

# Oakestra USENIX ATC 2023 Artifacts 

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

Our artifact repositories for reproducing the experiments and results in the paper are organized as follows. 

<img src="https://github.com/oakestra/USENIX-ATC23-Oakestra-Artifacts/assets/5736850/73baf8e0-621a-4e16-844c-a480e0040912" width="60%" />

1. [**This**] [Main repository](https://github.com/oakestra/USENIX-ATC23-Oakestra-Artifacts/tree/main/Experiments): The repository contains the Root & Cluster orchestrators folders, as well as the Node Engine source code for the worker node.

2. [Network repository](https://github.com/oakestra/USENIX-ATC23-Oakestra-net-Artifacts): This repository contains the  Root, Cluster, and Worker network components.

3. [Experiments repository](https://github.com/oakestra/USENIX-ATC23-Oakestra-Artifacts/tree/main/Experiments): This repository is a sub-directory within this repo at `Experiments/` and includes the setup instructions to create your first Oakestra infrastructure and a set of scripts to automate the results collection procedure and reproduce our results.

4. [_Optional_] [Dashboard](https://github.com/oakestra/dashboard): The repository contains a front-end application that can be used to graphically interact with the platform. Its optional but gives a nice web-based GUI to Oakestra

---

# Getting Started

## Set up the infrastructure

We offer three distinct possibilities for setting up Oakestra infrastructure.

### I. Single-node Infrastructure

<img src="https://github.com/oakestra/USENIX-ATC23-Oakestra-Artifacts/assets/5736850/e33c6788-d5bd-4684-a6f1-120abab9001d" width="30%" />

The most straightforward infrastructure setup is the single cluster and single worker node deployment of Oakestra. All the components are deployed inside the same machine; this setup is recommended for testing and development purposes. We provide an Oakestra VM configured like this scenario which you can find [here](https://bit.ly/oakestra-artifacts).

**Disclaimer:** Please bear in mind that some of the experiments, like the stress test \cref{sec:stresstest} and the AR pipeline \cref{sec:arpipeline}, require adequate hardware to run in a single node setup. In this case, we recommend 16 GB of RAM and 16 core CPU. 
 
### II. Separate Worker Infrastructure

<img src="https://github.com/oakestra/USENIX-ATC23-Oakestra-Artifacts/assets/5736850/553230cf-21c6-4786-a2c1-2786566a5026" width="30%" />

A worker node is an external machine (machine 2) connected to the control plane (machine 1). This setup is recommended if you want to get started with a small cluster because it enables horizontal scalability by introducing more worker nodes (on multiple Linux machines) attached to the same master (machine 1). 

### III. Multiple Machine Infrastructure

<img src="https://github.com/oakestra/USENIX-ATC23-Oakestra-Artifacts/assets/5736850/b4800423-b4d0-4f27-b4df-82fb6c7a20c4" width="30%" />

This is a single cluster setup but with the separation of the Root and Cluster control plane on 2 different machines. This setup is recommended if one foresees a multi-cluster deployment in the future because new machines with new cluster orchestrators and worker nodes can be connected to the root orchestrator deployed in machine 1.

## Hardware Requirements

### Scenario 1

- `AMD64` `x86-64` Machine
  - 8 GB of RAM
  - 50 GB Disk space
  - 8 cores CPU
 
### Scenario 2 & Scenario 3

- **Root Orchestrator**
  - 2GB of RAM
  - 2 Core CPU, ARM64 or AMD64 architecture
  - 10GB disk
      - tested on: Ubuntu 20.20, Windows 10, MacOS Monterey
        
- **Cluster Orchestrator**
  - 2GB of RAM
  - 2 Core CPU, ARM64 or AMD64 architecture
  - 5GB disk
      - tested on: Ubuntu 20.20, Windows 10, MacOS Monterey
 
- **Worker Node**
  - Linux-based OS
  - 2 Core CPU, ARM64 or AMD64 architecture
  - 2GB disk
  - `iptables`

> Network requirements
> - Root Orchestrator and Cluster orchestrator must be mutually reachable
> - Cluster orchestrator must be reachable from the Worker node
> - Each worker exposes port 50103 for tunneling
> - Root and cluster orch expose ports in the range: 10000-12000, 80

## Step-by-Step Instructions

We have created a detailed `README` and `getting-started` guide that provides step-by-step instructions which you can find [here](https://github.com/oakestra/USENIX-ATC23-Oakestra-Artifacts/blob/main/Experiments/README.pdf). Please follow the instructions provided in _Section 4_ of the `README` file.



## Networking 

Please see [Oakestra Net Artficat Repository](https://github.com/oakestra/USENIX-ATC23-Oakestra-net-Artifacts) for setting up networking.

## Frontend?

To make your life easier you can run the Oakestra front-end.
Please check the [Dashboard](https://github.com/oakestra/dashboard) repository for more information.

# Beyond the paper

This repository is recreating our USENIX ATC artifacts and is, therefore, out-of-sync of the main Oakestra development. Please see the `main` [Oakestra](https://github.com/oakestra/oakestra) for the latest features.

