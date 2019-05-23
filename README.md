# Prediction API
## Introduction

_AMiner Prediction API_ is a toolkit for science data prediction, such as scholar portrait property prediction. The toolkit aims to utilize science data and machine learning algorithms to provide more intelligent functionality for global researchers. All algorithms and models which the toolkit uses are derived from [AMiner](https://aminer.cn).

## Pre-requirement

[`anaconda`](https://www.anaconda.com/) is strongly recommended for environment configuration. Additionally, some libraries are requied:

* [`fasttext`](https://fasttext.cc/)
* [`scikit-learn`](https://scikit-learn.org/)
* [`jieba`](https://github.com/fxsjy/jieba)
* [`requests`](https://2.python-requests.org/)

Use following commands to install these libraries:

### windows/linux

```bash
conda install -c mbednarski fasttext
conda install -c anaconda scikit-learn
conda install -c conda-forge jieba
conda install -c conda-forge requests
```

### osx

```bash
conda install -c conda-forge fasttext
conda install -c anaconda scikit-learn
conda install -c conda-forge jieba
conda install -c conda-forge requests
```

## Models Download

Toolkit depends on some pre-trained model files which can be downloaded at following address:

[Download](https://lfs.aminer.cn/misc/model.zip)

Extract it and move all files into `model` directory before testing code.
