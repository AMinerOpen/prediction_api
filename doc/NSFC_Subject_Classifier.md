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

### https://innovaapi.aminer.cn/tools/v1/predict/nsfc

![](https://img.shields.io/badge/http-post-blue.svg)

An online version of the method "classify"

#### Request body

##### titles

A **list** of **strings**. The titles of publications.

#### An example

```http
POST /tools/v1/predict/nsfc? HTTP/1.1
Host: innovaapi.aminer.cn
Content-Type: application/json
cache-control: no-cache
Postman-Token: 0d145f77-f3d7-4bf0-8521-f22d2d008ba0

{
    "titles": [
        "On the Power of Massive Text Data.",
        "GeoBurst+: Effective and Real-Time Local Event Detection in Geo-Tagged Tweet Streams.",
        "Entity Set Search of Scientific Literature: An Unsupervised Ranking Approach.",
        "CoType: Joint Extraction of Typed Entities and Relations with Knowledge Bases.",
        "PRED: Periodic Region Detection for Mobility Modeling of Social Media Users."
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
                "code": "A03",
                "name": "天文学",
                "p": 0.07537554949522018
            },
            {
                "code": "C06",
                "name": "遗传学与生物信息学",
                "p": 0.07491405308246613
            },
            {
                "code": "H31",
                "name": "药理学",
                "p": 0.0605212077498436
            },
            {
                "code": "C05",
                "name": "生物物理、生物化学与分子生物学",
                "p": 0.053404878824949265
            },
            {
                "code": "D02",
                "name": "地质学",
                "p": 0.05324738845229149
            }
        ],
        "level2": [
            {
                "code": "D0309",
                "name": "环境地球化学",
                "p": 0.07380235195159912
            },
            {
                "code": "E0804",
                "name": "环境工程",
                "p": 0.0457393117249012
            },
            {
                "code": "E0405",
                "name": "露天开采与边坡工程",
                "p": 0.04072700813412666
            },
            {
                "code": "H3105",
                "name": "抗肿瘤药物药理",
                "p": 0.03553887456655502
            },
            {
                "code": "C0403",
                "name": "动物生理及行为学",
                "p": 0.02961149252951145
            }
        ],
        "level3": [
            {
                "code": "C200703",
                "name": "食品生物污染与控制",
                "p": 0.17296439409255981
            },
            {
                "code": "C200102",
                "name": "粮油食品原料学",
                "p": 0.14757823944091797
            },
            {
                "code": "A030302",
                "name": "变星和激变变星、双星和多星系统",
                "p": 0.14537328481674194
            },
            {
                "code": "E080402",
                "name": "污水处理与资源化",
                "p": 0.05403073877096176
            },
            {
                "code": "C050604",
                "name": "电离辐射生物物理与放射生物学",
                "p": 0.05319990590214729
            }
        ]
    }
}
```

### https://innovaapi.aminer.cn/tools/v1/predict/nsfc/person

![](https://img.shields.io/badge/http-get-brightgreen.svg)

Get a professor's research interests according to his publications' titles.

#### Parameters

pid: the professor's id in [AMiner](https://aminer.cn).

For example, you want to know Qiang Yang's research interests. First, you should search Qiang Yang in  [AMiner](https://aminer.cn), and get his page url https://www.aminer.cn/profile/qiang-yang/53f48041dabfae963d25910a. His id in [AMiner](https://aminer.cn) is the suffix of the url string `53f48041dabfae963d25910a`.

#### An example

https://innovaapi.aminer.cn/tools/v1/predict/nsfc/person?pid=53f48041dabfae963d25910a

## Accuracy

| level |  top1  |  top5  |
| :---: | :----: | :----: |
|   1   | 0.5079 | 0.8331 |
|   2   | 0.3629 | 0.6668 |
|   3   | 0.3342 | 0.6317 |

