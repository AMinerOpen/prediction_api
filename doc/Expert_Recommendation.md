# Expert recommendation

## Introduction

ExpertRec is a class which is used to recommend some experts in the given text's field.

## Method

### search

```python
search(text, num=20)
```

#### Introduction

Recommend some experts in the given text's field.

#### Parameters

##### text

The text.

##### num

The number of the recommended experts.

#### Return value

 A list of dictionaries:

```python
{
    'id': The expert's ID in AMiner(http://www.aminer.cn/),
    'url': The expert's AMiner homepage.
    'L2 distance': Similarity. The smaller the L2 distance is , the more likely the expert is interested in the given text's field.
}
```

#### An example

```python
e = ExpertRec()
rt = e.search('natural language processing')
```

`rt`:

```python
[
    {
        'id': '544572eddabfae862da1d4e0', 
        'url': 'http://www.aminer.cn/profile/544572eddabfae862da1d4e0', 
        'L2 distance': 0.0
    }, 
    {
        'id': '53f438eadabfaee0d9b7cce4', 
        'url': 'http://www.aminer.cn/profile/53f438eadabfaee0d9b7cce4', 
        'L2 distance': 0.26824072
    }, 
    {
        'id': '53f432cbdabfaeb1a7bcfd9a', 
        'url': 'http://www.aminer.cn/profile/53f432cbdabfaeb1a7bcfd9a', 
        'L2 distance': 0.31506824
    }, 
    {
        'id': '53f432b7dabfaeb2ac02dc61',
        'url': 'http://www.aminer.cn/profile/53f432b7dabfaeb2ac02dc61',
        'L2 distance': 0.3284118
    }, 
    {
        'id': '53f43757dabfaeecd696742f', 
        'url': 'http://www.aminer.cn/profile/53f43757dabfaeecd696742f',
		'L2 distance': 0.34276736
    }
]
```

## API

### https://innovaapi.aminer.cn/tools/v1/predict/experts

![](https://img.shields.io/badge/http-post-blue.svg)

An online version of method `search`

#### Request body

##### text

The text

##### num

The number of the recommended experts.

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
POST /tools/v1/predict/experts? HTTP/1.1
Host: innovaapi.aminer.cn
Content-Type: application/json
User-Agent: PostmanRuntime/7.13.0
Accept: */*
Cache-Control: no-cache
Postman-Token: 05b4af12-9cf0-4cf9-a45c-6f8fd2a9d0a9,867a4a93-f753-4799-9aa9-96b8208f5067
Host: innovaapi.aminer.cn
accept-encoding: gzip, deflate
content-length: 60
Connection: keep-alive
cache-control: no-cache

{
    "text": "natural language processing",
    "num": 20
}
```

`Response`：

```json
{
    "status": 0,
    "message": "success",
    "data": [
        {
            "id": "544572eddabfae862da1d4e0",
            "url": "http://www.aminer.cn/profile/544572eddabfae862da1d4e0",
            "L2 distance": 0
        },
        {
            "id": "53f438eadabfaee0d9b7cce4",
            "url": "http://www.aminer.cn/profile/53f438eadabfaee0d9b7cce4",
            "L2 distance": 0.27
        },
        {
            "id": "53f432cbdabfaeb1a7bcfd9a",
            "url": "http://www.aminer.cn/profile/53f432cbdabfaeb1a7bcfd9a",
            "L2 distance": 0.32
        },
        {
            "id": "53f432b7dabfaeb2ac02dc61",
            "url": "http://www.aminer.cn/profile/53f432b7dabfaeb2ac02dc61",
            "L2 distance": 0.33
        },
        {
            "id": "53f43757dabfaeecd696742f",
            "url": "http://www.aminer.cn/profile/53f43757dabfaeecd696742f",
            "L2 distance": 0.34
        },
        {
            "id": "53f556d8dabfae963d25e88d",
            "url": "http://www.aminer.cn/profile/53f556d8dabfae963d25e88d",
            "L2 distance": 0.35
        },
        {
            "id": "53f4dc08dabfaef7e077b586",
            "url": "http://www.aminer.cn/profile/53f4dc08dabfaef7e077b586",
            "L2 distance": 0.35
        },
        {
            "id": "5448db69dabfae87b7e87eb5",
            "url": "http://www.aminer.cn/profile/5448db69dabfae87b7e87eb5",
            "L2 distance": 0.38
        },
        {
            "id": "53f430c6dabfaeb2ac014a3a",
            "url": "http://www.aminer.cn/profile/53f430c6dabfaeb2ac014a3a",
            "L2 distance": 0.39
        },
        {
            "id": "53f42cebdabfaee02ac5a471",
            "url": "http://www.aminer.cn/profile/53f42cebdabfaee02ac5a471",
            "L2 distance": 0.4
        },
        {
            "id": "53f43940dabfaefedbae3ddb",
            "url": "http://www.aminer.cn/profile/53f43940dabfaefedbae3ddb",
            "L2 distance": 0.4
        },
        {
            "id": "53f44514dabfaee43ec789c9",
            "url": "http://www.aminer.cn/profile/53f44514dabfaee43ec789c9",
            "L2 distance": 0.41
        },
        {
            "id": "53f4616fdabfaee4dc839eba",
            "url": "http://www.aminer.cn/profile/53f4616fdabfaee4dc839eba",
            "L2 distance": 0.41
        },
        {
            "id": "53f7c250dabfae938c6d865c",
            "url": "http://www.aminer.cn/profile/53f7c250dabfae938c6d865c",
            "L2 distance": 0.41
        },
        {
            "id": "53f43403dabfaee1c0a86645",
            "url": "http://www.aminer.cn/profile/53f43403dabfaee1c0a86645",
            "L2 distance": 0.41
        },
        {
            "id": "53f44194dabfaee2a1d254c8",
            "url": "http://www.aminer.cn/profile/53f44194dabfaee2a1d254c8",
            "L2 distance": 0.41
        },
        {
            "id": "53f430dddabfaeb1a7bb7664",
            "url": "http://www.aminer.cn/profile/53f430dddabfaeb1a7bb7664",
            "L2 distance": 0.41
        },
        {
            "id": "542c4a3bdabfae2b4e1fe347",
            "url": "http://www.aminer.cn/profile/542c4a3bdabfae2b4e1fe347",
            "L2 distance": 0.41
        },
        {
            "id": "53f482cedabfaec09f2a3dfb",
            "url": "http://www.aminer.cn/profile/53f482cedabfaec09f2a3dfb",
            "L2 distance": 0.42
        },
        {
            "id": "53f42945dabfaeb22f3d3d86",
            "url": "http://www.aminer.cn/profile/53f42945dabfaeb22f3d3d86",
            "L2 distance": 0.42
        }
    ]
}
```

