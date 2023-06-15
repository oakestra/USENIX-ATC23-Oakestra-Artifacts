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

There are a total of three artifact repositories for reproducing the experiments and results in the paper. 

1. [**This**] [Main repository](https://github.com/oakestra/USENIX-ATC23-Oakestra-Artifacts/tree/main/Experiments): The repository contains the Root & Cluster orchestrators folders, as well as the Node Engine source code for the worker node.

2. [Network repository](https://github.com/oakestra/USENIX-ATC23-Oakestra-net-Artifacts): This repository contains the  Root, Cluster, and Worker network components.

3. [Experiments repository](https://github.com/oakestra/USENIX-ATC23-Oakestra-Artifacts/tree/main/Experiments): This repository is a sub-directory within this repo at `Experiments/` and includes the setup instructions to create your first Oakestra infrastructure and a set of scripts to automate the results collection procedure and reproducing our results.

4. [_Optional_] [Dashboard](https://github.com/oakestra/dashboard): The repository contains a front-end application that can be used to graphically interact with the platform. Its optional but gives a nice web-based GUI to Oakestra

### Q. I want to recreate the experiments in the paper. What should I do?

A. We have created a detailed `README` and `getting-started` guide that provides step-by-step instructions which you can find [here](https://github.com/oakestra/USENIX-ATC23-Oakestra-Artifacts/blob/main/Experiments/README.pdf).

> We also provide a fully functional VM (OakestraVM.vmdk) with a single cluster and single node deployment of Oakestra. You can find the VM and all other artifacts [here](https://bit.ly/oakestra-artifacts).

### Q. I just want to try out Oakestra. Should I continue with this repo?

A. This repository is recreating our USENIX ATC artifacts and is, therefore, out-of-sync of the main Oakestra development. Please see the `main` [Oakestra](https://github.com/oakestra/oakestra) for the latest features.

---

# Getting Started

We offer three distinct possibilities for setting up Oakestra infrastructure.

<img src="https://github.com/oakestra/USENIX-ATC23-Oakestra-Artifacts/files/11760303/machine1.pdf" />

The most straightforward infrastructure setup is the \textbf{single cluster} and \textbf{single worker} node deployment of Oakestra. In \cref{fig:1machine}, all the components are deployed inside the same machine; this setup is recommended for testing and development purposes. We provide an Oakestra VM configured like this scenario (see \cref{sec:vm}).

[machine2.pdf](https://github.com/oakestra/USENIX-ATC23-Oakestra-Artifacts/files/11760307/machine2.pdf)
[machine3.pdf](https://github.com/oakestra/USENIX-ATC23-Oakestra-Artifacts/files/11760308/machine3.pdf)

## Networking 

Please see [Oakestra Net Artficat Repository](https://github.com/oakestra/USENIX-ATC23-Oakestra-net-Artifacts) for setting up networking.

## Frontend?

To make your life easier you can run the Oakestra front-end.
Please check the [Dashboard](https://github.com/oakestra/dashboard) repository for more information.


