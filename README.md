# Prediction API
![](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7-blue.svg)

## Introduction

_AMiner Prediction API_ is a toolkit for science data prediction, such as scholar portrait property prediction. The toolkit aims to utilize science data and machine learning algorithms to provide more intelligent functionality for global researchers. All algorithms and models which the toolkit uses are derived from [AMiner](https://aminer.cn).

## Pre-requirement

[`Anaconda`](https://www.anaconda.com/) is strongly recommended for environment configuration. Additionally, some libraries are requied. Use following commands to install these libraries:

|                           Library                            |                      Command                      |
| :----------------------------------------------------------: | :-----------------------------------------------: |
|              [`fastText`](https://fasttext.cc/)              |   `conda install -c mbednarski fasttext` *****    |
|         [`Scikit-learn`](https://scikit-learn.org/)          |     `conda install -c anaconda scikit-learn`      |
|          [`Jieba`](https://github.com/fxsjy/jieba)           |       `conda install -c conda-forge jieba`        |
|         [`Requests`](https://2.python-requests.org/)         |      `conda install -c conda-forge requests`      |
|            [`Tensorflow`](http://tensorflow.org/)            |     `conda install -c conda-forge tensorflow`     |
|               [`Pytorch`](http://pytorch.org/)               |        `conda install -c pytorch pytorch`         |
|              [`Numpy`](http://numpy.scipy.org/)              |       `conda install -c conda-forge numpy`        |
|            [`Pandas`](http://pandas.pydata.org/)             |       `conda install -c conda-forge pandas`       |
| [`BeautifulSoup4`](http://www.crummy.com/software/BeautifulSoup/) |   `conda install -c conda-forge beautifulsoup4`   |
|               [`Scrapy`](https://scrapy.org/)                |       `conda install -c conda-forge scrapy`       |
|                        `Levenshtein`                         | `conda install -c conda-forge python-levenshtein` |

> ***** If you are using **OSX**, you should use following command to intall `fastText`
>
> ```bash
> conda install -c conda-forge fasttext
> ```

## Models Download

Toolkit depends on some pre-trained model files which can be downloaded at following address:

[Download](https://lfs.aminer.cn/misc/model.zip)

Extract it and move all files into `model` directory before testing code.

## Document

[NSFC Subject Classifier](https://github.com/AMinerOpen/prediction_api/blob/master/doc/NSFC_Subject_Classifier.md)

[NSFC AI Subject Classifier](https://github.com/AMinerOpen/prediction_api/blob/master/doc/NSFC_AI_Subject_Classifier.md)

[Gender Prediction](https://github.com/AMinerOpen/prediction_api/blob/master/doc/Gender_Prediction.md)

[Identity Prediction](https://github.com/AMinerOpen/prediction_api/blob/master/doc/Identity_Prediction.md)

[Jobhopping Prediction](https://github.com/AMinerOpen/prediction_api/blob/master/doc/Jobhopping_Prediction.md)

[Expert Recommendation](https://github.com/AMinerOpen/prediction_api/blob/master/doc/Expert_Recommendation.md)

[Paper Ranker](https://github.com/AMinerOpen/prediction_api/blob/master/doc/Paper_Ranker.md)

