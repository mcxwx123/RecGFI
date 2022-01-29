# Replication Package for ICSE 2022 Paper "Recommending Good First Issues in GitHub OSS Projects"

This is the replication package for the ICSE 2022 paper *Recommending Good First Issues in GitHub OSS Projects*. It contains: 1) a dataset of 53,510 resolved issues; and 2) scripts to train different models and reproduce evaluation results, as described in the paper.

The package is stored in the git repository https://github.com/mcxwx123/RecGFI and permanently archived at [Zenodo](https://zenodo.org/record/5881117). To reproduce results in the paper, it is necessary to properly configure an Anaconda environment to run the scripts or use the VirtualBox VM Image we provide at [Zenodo](https://zenodo.org/record/5881117). 

## Introduction

In the ICSE 2022 paper, we propose **RecGFI**, an effective practical approach for automated recommendation of **Good First Issues** to OSS newcomers, which can be used to relieve maintainers’ burden and help newcomers onboard. 

For this purpose, we locate 100 newcomer-friendly GitHub projects, use GHTorrent and GitHub REST API to restore historical states of all their issues, and find issues resolved by newcomers. With the dataset, we check the performance of RecGFI under a variety of settings. Additionally, we collect latest open issues from the 100 projects and predict whether they are GFIs. We report potential GFIs to project maintainers and record the received responses and the state of these issues after several months.

All automated processing is implemented using Python in an Anaconda environment and the detailed results can be found in our paper. We hope the dataset and scripts in this replication package can be leveraged to facilitate further studies in recommending issues for newcomers and other related fields. We intend to claim the **Artifacts Available** badge and the **Artifacts Evaluated - Reusable** badge for our replication package. 

## Required Skills and Environment

For unobstructed usage of this replication package, we expect the user to have a reasonable amount of knowledge on git, Linux, Python, Anaconda, and some experience with Python data science development. 

We recommend to manually setup the required environment in a commodity Linux machine with at least 1 CPU Core, 8GB Memory and 100GB empty storage space. The package has also been vetted on Windows 10 with Anaconda.

## Replication Package Setup

In this section, we introduce how to set up the required environment for the reproducible results in the paper. First, clone this repository or download the repository archive from Zenodo.

Switch to the `RecGFI` folder. We use Anaconda for Python development. Configure a new Conda environment by executing the following commands:

```shell script
conda create -n RecGFI python=3.8
conda activate RecGFI
python -m pip install -r requirements-lock.txt
```

If you download repository archive from Zenodo, you can already find the issue dataset at `RecGFI/data/issuedata.json`.  However, it is too large (1.6GB) for git, so if you clone from GitHub, please download this file separately from Zenodo and put it there.

### Using the VirtualBox VM Image

To ease the burden to build the required environment, we supply a VirtualBox VM Image to replicate experimental results quickly and easily. You can download the VM Image from Zenodo. Then register and open it with VirtualBox VM. The password is icse22ae. You can see a folder named `RecGFI` in the Desktop with everything already configured. In a terminal, remember to use `conda activate RecGFI` to activate the corresponding Conda environment before executing the scripts below.

## Replicating Results

Switch your working directory to `RecGFI`. Run `Main.py` to get the performance results for RQ1 in our paper. 

```shell
python Main.py
```

During this process, some data preprocessing will take place. We leave the preprocessed data in the `RecGFI/data` folder. You can comment out the function calls `data_preprocess1()` and `data_preprocess2()` in `Main.py` if the preprocessed file already exists. The whole script can **consume up to 6GB memory and take up to five hours to finish**. It may generate some warning messages about logisitic regression but it is expected.

After running `Main.py`, you can get five CSV files in the folder `RecGFI/models`. They contain all tables for **RQ1** in the paper.

As for **RQ2**, you can check the statistics of issue features in our dataset with `RecGFI/data/Statistics.png`. After running `Main.py`, the wordclouds of issues is shown in `RecGFI/wordcloud0.png` and `RecGFI/wordcloud1.png`. You can also run `RecGFI/intepretation/Run_lime.py` which will generate the data for drawing figures in RQ2. 

```shell
cd intepretation
python Run_lime.py
```

The whole script can **take up to one day to finish**. It may generate some warning messages during the run. After running `Run_lime.py`, several `*.mat` files will be generated in `RecGFI/intepretation/data`. These files are already provided in our git repository. The `.m` files in `RecGFI/intepretation/draw_figs` can be executed with Matlab 2020b or higher version to draw the figures. However, Matlab is proprietary software. According to the requirments for "Resuable" badge, "Proprietary artifacts need not be included". Therefore, we do not intend to claim badges for the Matlab part of our replication package.

As for **RQ3**, we save the status of involved issues in `real_world_evaluation/prediction_real_world_issues.csv`. 
