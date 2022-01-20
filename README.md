# Replication Package for ICSE 2022 Paper "Recommending Good First Issues in GitHub OSS Projects"

This is the replication package for the ICSE 2021 paper *Recommending Good First Issues in GitHub OSS Projects*. It contains the collected dataset which can be used for future work and can be used to replicate experimental results in the paper. The replication package consists of a dataset including data about features and status (if an issue is closed by a newcomer) of issues from 100 popular and beginner-friendly projects, and scripts to predict wheyher issues will be solved by newcomers. People who want to reproduce the results in the paper need to properly configure an Anaconda environment to run the scripts or use the VirtualBox VM Image we provided.

## Introduction

Open Source Software (OSS) has become the infrastructure of our society. However, OSS are prone to sustainability failures, thus a large number of downstream clients may be impacted and suffer from severe losses. One way to promote OSS sustainability is to attract and retain capable newcomers to contribute to the projects. As a potentially beneficial measure to attract newcomers, GitHub recommends project maintainers to label issues as “Good First Issues” (GFIs), which is an explicit signal showing thatthis issue is suitable and welcome for newcomers to solve. Nevertheless, manually labeledGFIs are often highly insufficient and inappropriate for newcomers due to subjective bias of developers who labeled issues. To overcome these problems, we propose RecGFI, an effective practical approach forthe recommendation of good first issues to newcomers, which canbe used to relieve maintainers’ burden and help newcomers onboard. We evaluate RecGFI in two different scenarios by asking the following research questions in our ICSE 2022 paper:

* **RQ1:** How does RecGFI perform in predicting whether an issue is suitable for newcomers?
* **RQ2:** Is RecGFI helpful in a real world setting?

For RQ1, we use GHTorrent and Github API V3 to restore historical states of issues closed by commits or pull requests in 100 projects. With the dataset, we check the performance of RecGFI under three settings including different thresholds (the number of commits from a developer in a project to define newcomers), time-sorted issues and cross-prrojects settings. For RQ2, we collected the latest open issues from the 100 projects and predict whether they are GFIs. We report potential GFIs to project maintainers and record the received responces and the state of these issues after several months. All automated processing is implemented using Python in an Anaconda environment. The detailed results can be found in our paper. We hope the dataset and scripts in this replication package can be leveraged to facilitate further studies in recommending issues for newcomers and other related fields. We intend to claim the **Artifacts Available** badge and the **Artifacts Evaluated - Reusable** badge for our replication package. 

## Required Skills and Environment

For unobstructed usage of this replication package, we expect the user to have a reasonable amount of knowledge on git, Linux, Python, Anaconda, and some experience with Python data science development. 

We recommend to manually setup the required environment in a commodity Linux server with at least 1 CPU Core, 8GB Memory and 100GB empty storage space.

## Replication Package Setup

In this section, we introduce how to set up the required environment for the reproducible results in the paper.

We use Anaconda for Python development. The first step is to configure a new Conda environment. You can execute the following commands for such purpose:

```shell script
conda create -n RecGFI python=3.8
conda activate RecGFI
# We originally used requirements.txt as our dependency specification file,
# but in a clean installation, the installed packages may be later versions and contain breaking changes,
# so we created a lock file requirements-lock.txt to replicate our environment
python -m pip install -r requirements-lock.txt
# python -m pip install -r requirements.txt
```

Then clone this git repository or download the repository archive from Zenodo. You can find the raw dataset for RQ1 at RecGFI/data/issuedata.json. We record features and states of each issue at two time points. You can run Main.py to get the simulation results for RQ1 in our paper. We leave the preprocessed data in the file RecGFI/data. If you want to save time in preprocessing data, you can comment the functions `data_preprocess1()` and `data_preprocess2()`. As for RQ2(i.e. RQ3 in the paper), we store the status of the latest issues in prediction_real_world_issues.csv. You can execute the command `jupyter notebook` in the path RecGFI/real_world_evaluation to open a website and run `real_world_evaluation_results.ipynb`. Thus you can get statistics of the latest issues.

### Using the VirtualBox VM Image

To easy the burden to build the required environment, we supply a VirtualBox VM Image to replicate experimental results quickly and easily. You can download the VM Image from [the One Drive link](https://dreamok-my.sharepoint.com/:f:/g/personal/hehao_wowvv_com/EquUX-BJCjhOllxiNxA0ptkBDHTbDufze25oTK5SJOvlXg?e=bDJdUd). Then register and open it with VirtualBoxVM. The passport is icse22ae. You can see a folder named `RecGFI` in the Desktop. Open and run RecGFI/Main.py with VSCode or Terminal to get the results for RQ1. Then execute the command `jupyter notebook` and run `real_world_evaluation_results.ipynb` to get the results for RQ2. Note that this way for replication is non-persistent. If the VM Image is not available, please switch to other ways.

## Replicating Results

You can get five csv files in the folder RecGFI/models by running Main.py. They contain all tables for RQ1 in the paper. As for RQ2 in the paper, you can check the statistics of issue features in our dataset with RecGFI/data/Statistics.png. The raw data for RQ3 in the paper is recorded in RecGFI/real_world_evaluation/prediction_real_world_issues.csv. You can see the statistics of the latest issues shown in the RQ3 of our paper in the cells' output of the notebook `real_world_evaluation_results.ipynb`.
