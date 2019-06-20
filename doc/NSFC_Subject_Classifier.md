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

##### translation_func

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
pub_titles = ['基于多通道卷积神经网络的中文微博情感分析']
subject = nsfc.classify(pub_titles)
```

`subject`:

```python
{
    'level1': [
        {'code': 'F02', 'name': '计算机科学', 'p': 0.9745969772338867},
        {'code': 'F01', 'name': '电子学与信息系统', 'p': 0.02385014481842518},
        {'code': 'B05', 'name': '分析化学', 'p': 0.0005464374553412199},
        {'code': 'F03', 'name': '自动化', 'p': 0.00039022043347358704},
        {'code': 'H18', 'name': '影像医学与生物医学工程', 'p': 0.0001973187318071723}
    ], 
    'level2': [
        {'code': 'F0206', 'name': '自然语言理解与机器翻译', 'p': 0.8545559048652649},
        {'code': 'F0205', 'name': '计算机应用技术', 'p': 0.08089018613100052},
        {'code': 'F0305', 'name': '人工智能与知识工程', 'p': 0.023599255830049515},
        {'code': 'B0512', 'name': '化学计量学与化学信息学', 'p': 0.0228357}
    ], 
    'level3': [
        {'code': 'F020601', 'name': '计算语言学', 'p': 0.9999170303344727},
        {'code': 'F020504', 'name': '生物信息计算', 'p': 4.625070505426265e-05},
        {'code': 'F020506', 'name': '人机界面技术', 'p': 2.3111495465855114e-05},
        {'code': 'F010403', 'name': '物联网', 'p': 2.2251791961025447e-05},
        {'code': 'F010303', 'name': '协作通信', 'p': 2.0015930203953758e-05}
    ]
}
```

## API

### https://innovaapi.aminer.cn/tools/v1/predict/nsfc

![](https://img.shields.io/badge/http-post-blue.svg)

An online version of the method `classify`

#### Request body

##### titles

A **list** of **strings**. The titles of publications.

#### Return value

In the `Response` object, there will be three fields.

##### status

`0`: Success

`1`: There are some errors.

##### message

`success`: Success

If there are some errors, you will get the error information.

##### data

The return value from the method.

#### An example

```http
POST /tools/v1/predict/nsfc? HTTP/1.1
Host: innovaapi.aminer.cn
Content-Type: application/json
User-Agent: PostmanRuntime/7.13.0
Accept: */*
Cache-Control: no-cache
Postman-Token: 5f0fbe87-e333-40b1-b9c3-23f64c137c15,1927af8e-4a86-4319-8024-684d6b9e46f7
Host: innovaapi.aminer.cn
accept-encoding: gzip, deflate
content-length: 100
Connection: keep-alive
cache-control: no-cache

{
    "titles": [
        "基于多通道卷积神经网络的中文微博情感分析"
    ]
}
```

Return Message:

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "level1": [
            {
                "code": "F02",
                "name": "计算机科学",
                "p": 0.9745969772338867
            },
            {
                "code": "F01",
                "name": "电子学与信息系统",
                "p": 0.02385014481842518
            },
            {
                "code": "B05",
                "name": "分析化学",
                "p": 0.0005464374553412199
            },
            {
                "code": "F03",
                "name": "自动化",
                "p": 0.00039022043347358704
            },
            {
                "code": "H18",
                "name": "影像医学与生物医学工程",
                "p": 0.0001973187318071723
            }
        ],
        "level2": [
            {
                "code": "F0206",
                "name": "自然语言理解与机器翻译",
                "p": 0.8545559048652649
            },
            {
                "code": "F0205",
                "name": "计算机应用技术",
                "p": 0.08089018613100052
            },
            {
                "code": "F0305",
                "name": "人工智能与知识工程",
                "p": 0.023599255830049515
            },
            {
                "code": "B0512",
                "name": "化学计量学与化学信息学",
                "p": 0.022835755720734596
            },
            {
                "code": "F0104",
                "name": "通信网络",
                "p": 0.01253295037895441
            }
        ],
        "level3": [
            {
                "code": "F020601",
                "name": "计算语言学",
                "p": 0.9999170303344727
            },
            {
                "code": "F020504",
                "name": "生物信息计算",
                "p": 0.00004625070505426265
            },
            {
                "code": "F020506",
                "name": "人机界面技术",
                "p": 0.000023111495465855114
            },
            {
                "code": "F010403",
                "name": "物联网",
                "p": 0.000022251791961025447
            },
            {
                "code": "F010303",
                "name": "协作通信",
                "p": 0.000020015930203953758
            }
        ]
    }
}
```

### https://innovaapi.aminer.cn/tools/v1/predict/nsfc/person

![](https://img.shields.io/badge/http-get-brightgreen.svg)

Get a professor's research interests according to his publications' titles.

#### Parameters

##### pid

the professor's id in [AMiner](https://aminer.cn).

For example, you want to know Qiang Yang's research interests. First, you should search Qiang Yang in  [AMiner](https://aminer.cn), and get his page url https://www.aminer.cn/profile/qiang-yang/53f48041dabfae963d25910a. His id in [AMiner](https://aminer.cn) is the suffix of the url string `53f48041dabfae963d25910a`.

#### Return value

In the `Response` object, there will be three fields.

##### status

`0`: Success

`1`: There are some errors.

##### message

`success`: Success

If there are some errors, you will get the error information.

##### data

The return value from the method.

#### An example

https://innovaapi.aminer.cn/tools/v1/predict/nsfc/person?pid=53f48041dabfae963d25910a

## Accuracy

| level |  top1  |  top5  |
| :---: | :----: | :----: |
|   1   | 0.5079 | 0.8331 |
|   2   | 0.3629 | 0.6668 |
|   3   | 0.3342 | 0.6317 |

