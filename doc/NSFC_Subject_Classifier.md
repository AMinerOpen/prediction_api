# NSFC Subject Classifier

## Introduction

Classifier is a class which is used to classify publications according to their subjects. It depends on the classification of [Natural Science Foundation of China(NSFC)](http://www.nsfc.gov.cn/nsfc/cen/xmzn/2019xmzn/15/index.html). 

## Method

### classify

```python
classify(pub_titles, level=0, ntop=5, lang_zh=False, translatation_func=youdao_translate)
```
#### Introduction

Use publications' titles to classify which subjects these publications belong to.

#### Parameters

##### pub_titles

A **list** of **strings**. The titles of publications.

##### level

Classification level(1,2,3), for other numbers you will get all three levels.

[NSFC](http://www.nsfc.gov.cn/nsfc/cen/xmzn/2019xmzn/15/index.html) uses a three-level classification. Use graph theory as an example, 

```
A01 mathematics
- A0116 combinatorial mathematics
  - A011602 graph theory
```

##### ntop

The number of possible subjects you want to get.

##### lang_zh

Whether the titles are Chinese or not. For `True`, it means you are using Chinese publications.

##### tranaltion_func

In fact, the classifier can only work on **Chinese** words because of the classification standard and the training data. In order to handle publications in other languages, you need to provide a translation function.  It should be able to translate a list of **strings** in another language to Chinese.

In default, we provide a translator based on [youdao api](http://fanyi.youdao.com/).  But you cannot use this translator too often because it is only a free version. 

#### Return value

A **dictionary**

```python
'level{x}'(x = 1, 2, 3)':
{
    'code': subject code
    'name': subject name
    'p': probability
}
```

If there are some errors in the method, you will get a `{}`

#### An example

```python
nsfc = Classifier()
pub_titles = ['Annotating gene sets by mining large literature collections with protein networks.']
subject = nsfc.classify(pub_titles)
```

subject:

```python
{
    'level1': [
        {'code': 'F03', 'name': '自动化', 'p': 0.5681461691856384},
        {'code': 'B06', 'name': '化学工程及工业化学', 'p': 0.06985147297382355},
        {'code': 'E04', 'name': '冶金与矿业', 'p': 0.05790099501609802},
        {'code': 'F02', 'name': '计算机科学', 'p': 0.04791523516178131},
        {'code': 'C13', 'name': '农学基础与作物学', 'p': 0.04653266444802284}
    ], 
    'level2': [
        {'code': 'A0114', 'name': '应用数学方法', 'p': 0.5198239684104919},
        {'code': 'C1301', 'name': '农学基础', 'p': 0.2457106113433838},
        {'code': 'C0505', 'name': '系统生物学', 'p': 0.03674702346324921},
        {'code': 'F0302', 'name': '系统科学与系统工程', 'p': 0.034390855580568314},
        {'code': 'C1004', 'name': '生物电子学', 'p': 0.0336870439350605}
    ], 
    'level3': [
        {'code': 'A011403', 'name': '生物数学', 'p': 0.9948329925537109},
        {'code': 'A011405', 'name': '分形论及应用', 'p': 0.005175579339265823},
        {'code': 'F030204', 'name': '系统生物学中的复杂性分析与建模', 'p':1.471634732e-05},
        {'code': 'F030114', 'name': '自适应与学习控制', 'p': 1.187794805446174e-05},
        {'code': 'A011004', 'name': '极限理论', 'p': 1.175022862298647e-05
        }
    ]
}
```

## API

### classify

![](https://img.shields.io/badge/http-post-blue.svg)

https://innovaapi.aminer.cn/tools/v1/predict/nsfc

## Accuracy

| level |  top1  |  top5  |
| :---: | :----: | :----: |
|   1   | 0.5079 | 0.8331 |
|   2   | 0.3629 | 0.6668 |
|   3   | 0.3342 | 0.6317 |

