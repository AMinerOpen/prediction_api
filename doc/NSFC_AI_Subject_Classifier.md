# NSFC AI Subject Classifier

## Introduction

AIClassifier is a class which is used to classify AI subjects according to some keywords. It depends on the classification of [Natural Science Foundation of China(NSFC)](http://www.nsfc.gov.cn/nsfc/cen/xmzn/2019xmzn/15/index.html). 

## Method

### get_tree

```python
get_tree(words):
```

#### Introduction

Get a subject tree according to some keywords.

#### Parameters

##### words

A **list** of keywords.

#### Return value

A list of **dictionary**

```python
[
    {
        "name": subject name,
        "value": probability,
        "children": subtrees. They also have the same structure. If this is a leaf node, it won't have this field
    }
]
```

#### An example

```python
ai_nsfc = AIClassifier()
words = ['search engine']
subject = ai_nsfc.get_tree(words)
print(subject)
```

Return value:

```python
[
    {
        'name': '人工智能', 
        'value': 1.0, 
        'children': [
            {
                'name': '自然语言处理', 
                'value': 0.6236383458601308, 
                'children': [
                    {'name': '文本检索、挖掘与信息抽取', 'value': 0.6106190412551927}
                ]
            },
            {
                'name': '知识表示与处理', 
                'value': 0.3763616541398693, 
                'children': [
                    {'name': '知识发现与数据挖掘', 'value': 0.3893809587448072}
                ]
            }
        ]
    }
]
```

### classify_level

```python
classify_level(words, level=1, lang_zh=False):
```

#### Introduction

 Classify which subjects these keywords belong to.

#### Parameters

##### words

A **list** of keywords.

##### level

Classification level(1,2,3), for other numbers you will get a  `[]`.

[NSFC](http://www.nsfc.gov.cn/nsfc/cen/xmzn/2019xmzn/15/index.html) uses a three-level classification. Use graph theory as an example, 

```
A01 mathematics
- A0116 combinatorial mathematics
  - A011602 graph theory
```

##### lang_zh

Whether the return values are Chinese or not.

#### Return Value

A **list** of strings contains related subject names at the level

#### An example

```python
ai_nsfc = AIClassifier()
words = ['search engine']
subject = ai_nsfc.classify_level(words, level=3)
print(subject)
```

Return Value:

```python
['Text Retrieval, Mining And Information Extraction', 'Knowledge Discovery And Data Mining']
```

### classify

 Get the classification of the keywords and a subject tree

#### Parameters

##### words

A **list** of keywords. Accept both Chinese words and English words.

#### Return value

A dictionary contains four items:

```
'level{x}'(x = 1, 2, 3): Related subjects of the words on level x.
'tree': Subject trees of the given words(a list of dictionary).
```

#### An example

```python
ai_nsfc = AIClassifier()
words = ['search engine']
subject = ai_nsfc.classify(words)
print(subject)
```

Return Value:

```python
{
    'level1': [
        {'p': 1.0, 'name': 'Artificial Intelligence', 'name_zh': '人工智能'}
    ], 
    'level2': [
        {'p': 0.6236383458601308,'name': 'Natural Language Processing', 'name_zh': '自然语言处理'},
        {'p': 0.3763616541398693, 'name': 'Knowledge Representation And Processing', 'name_zh': '知识表示与处理'}
    ], 
    'level3': [
        {'p': 0.6106190412551927, 'name': 'Text Retrieval, Mining And Information Extraction', 'name_zh': '文本检索、挖掘与信息抽取'},
        {'p': 0.3893809587448072, 'name': 'Knowledge Discovery And Data Mining', 'name_zh': '知识发现与数据挖掘'}
    ], 
    'tree': [
        {
            'name': '人工智能', 
            'value': 1.0, 
         	'children': [
                {
                    'name': '自然语言处理', 
                    'value': 0.6236383458601308, 
                    'children': [
                        {'name': '文本检索、挖掘与信息抽取', 'value': 0.6106190412551927}
                    ]
                },
                {
                    'name': '知识表示与处理', 
                    'value': 0.3763616541398693, 
                    'children': [
                        {'name': '知识发现与数据挖掘', 'value': 0.3893809587448072}
                    ]
                }
            ]
        }
    ]
}
```

## API

### https://innovaapi.aminer.cn/tools/v1/predict/nsfc/ai

![](https://img.shields.io/badge/http-post-blue.svg)

An online version of the method "classify"

### Request body

##### words

A **list** of key words. Accept both Chinese words and English words.

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

### An example

```http
POST /tools/v1/predict/nsfc/ai? HTTP/1.1
Host: innovaapi.aminer.cn
Content-Type: application/json
User-Agent: PostmanRuntime/7.13.0
Accept: */*
Cache-Control: no-cache
Postman-Token: 72d90554-ead1-4606-be9e-ce64a9b38391,354aaeaa-976a-406c-902b-d3d1e52389f7
Host: innovaapi.aminer.cn
accept-encoding: gzip, deflate
content-length: 49
Connection: keep-alive
cache-control: no-cache

{
    "words": [
            "search engine"
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
                "p": 1.0,
                "name": "Artificial Intelligence",
                "name_zh": "人工智能"
            }
        ],
        "level2": [
            {
                "p": 0.6236383458601308,
                "name": "Natural Language Processing",
                "name_zh": "自然语言处理"
            },
            {
                "p": 0.3763616541398693,
                "name": "Knowledge Representation And Processing",
                "name_zh": "知识表示与处理"
            }
        ],
        "level3": [
            {
                "p": 0.6106190412551927,
                "name": "Text Retrieval, Mining And Information Extraction",
                "name_zh": "文本检索、挖掘与信息抽取"
            },
            {
                "p": 0.3893809587448072,
                "name": "Knowledge Discovery And Data Mining",
                "name_zh": "知识发现与数据挖掘"
            }
        ],
        "tree": [
            {
                "name": "人工智能",
                "value": 1.0,
                "children": [
                    {
                        "name": "自然语言处理",
                        "value": 0.6236383458601308,
                        "children": [
                            {
                                "name": "文本检索、挖掘与信息抽取",
                                "value": 0.6106190412551927
                            }
                        ]
                    },
                    {
                        "name": "知识表示与处理",
                        "value": 0.3763616541398693,
                        "children": [
                            {
                                "name": "知识发现与数据挖掘",
                                "value": 0.3893809587448072
                            }
                        ]
                    }
                ]
            }
        ]
    }
}
```

