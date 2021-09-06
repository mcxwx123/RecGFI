# Recommending Good First Issues in GitHub OSS Projects

## Dataset
We collected 53,510 issues closed by commit or pull request for 100 projects. The data of these issues are stored in /data/data.npy.

The snapshots of issues at two time points (when issues are created and before some developer starts to work on issues) are generated with data_preprocess_1.py and data_preprocess_2.py respectively.

## Models
The codes of experiments are placed in folder /models.

You can run RecGFI after the data is processed by data_preprocess_1.py and data_preprocess_2.py, to get all experimental results for RecGFI and its variants under different threshold k. The code of logistic regression and random forest are also provided for comparison.

The interpretable analysis of RecGFI's prediction results is realizsed by Interpreter_lime.py.

## Environment Setup

```shell
conda create -n GFI python=3.8
conda activate GFI
pip install -r requirements.txt
```

## Real World Evaluation
The results of real world evaluation are shown in the folder real_world_evaluation.
