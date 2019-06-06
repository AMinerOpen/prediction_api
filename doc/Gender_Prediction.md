# Gender Prediction

## Introduction

Gender is a class which is used to predict a person's gender.

If you want to use face detection to help you predict a person's gender, you can get an api-key from [Face++]( https://console.faceplusplus.com/documents/7079083), and then put the api-key into the `config.py`

## Method

### predict

```python
predict(self, name, org, source='google', image_url=None, image_file=None)
```

#### Introduction

Predict a person's gender.  We use name, results from search engine and the person's photo as features to predict his or her gender. About the photos, you can choose either online photos or local photos.

#### Parameters

##### name

**string**, the person's name

##### org

**string**, the person's organization

##### source

Use `google` or `baidu` as the search engine.

It is strongly recommended to use Google because the model is trained accoring to the results from Google.

##### image_url

The photo's online url.

##### image_file

The photo's local path.

#### An example

```python
g = Gender()
gen = g.predict(name='Jie Tang', org='Tsinghua University', image_url='http://www.cs.tsinghua.edu.cn/publish/cs/4616/20110330101939787483549/20190321114128398502759.jpg')
```

gen:

```python
{   
    'name': {
        'male': 0.5, 
        'female': 0.5
    }, 
    'search': {
        'male': 0.9173952287088033, 
        'female': 0.0826047712911967
    }, 
    'face': {
        'male': 1, 
        'female': 0
    }, 
    'male': 0.96, 
    'female': 0.04
}
```

## API

### https://innovaapi.aminer.cn/tools/v1/predict

![](https://img.shields.io/badge/http-get-brightgreen.svg)

An online version of the method `predict`

#### Parameters

##### name

**string**, the person's name

##### org

**string**, the person's organization

##### image_url

The photo's online url.

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

https://innovaapi.aminer.cn/tools/v1/predict/gender?name=Feifei%20Li&org=Stanford%20University

`Response`:

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "male": 0.07,
        "female": 0.93,
        "name": {
            "male": 0,
            "female": 1
        },
        "search": {
            "male": 0.13,
            "female": 0.87
        },
        "face": {
            "male": 0.5,
            "female": 0.5
        }
    }
}
```

