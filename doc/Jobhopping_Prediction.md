# Jobhopping Prediction

## Introduction

JobHopping is a class which is used to predict where a scholar may hop to.

## Method

### predict

```python
predict(name_squence, ntop=3)
```

#### Introduction

Get a scholar's possible future affiliation according to a list(squence) of affiliation's name  where he had worked.

#### Parameters

##### name_squence

a list of the scholar's institution he had worded

##### ntop

How many possible affiliations will the method return.

#### Return value

A list of dictionaries

```python
 {
     'name': the most likely future affiliation's name
     'p': the probability
 }
```

#### An example

```python
j = JobHopping()
aff = j.predict(['tsinghua university','mazandaran university','birsa agricultural university'])
```

`aff`:

```python
[
    {
        'name': 'university of michigan',
        'p': 0.33
    }, 
    {
        'name': 'university of cambridge',
        'p': 0.33
    }, 
    {
        'name': 'university of california berkeley',
        'p': 0.33
    }
]
```

## API

### https://innovaapi.aminer.cn/tools/v1/predict/career

![](https://img.shields.io/badge/http-get-brightgreen.svg)

An online version of method `predict`

#### Parameters
##### per_name

The scholar's name

##### org_name

The scholar's affiliation name

#### Return value

In the `Response` object, there will be three fields.

##### status

`0`: Success

`1`: There are some errors.

##### message

`success`: Success

If there are some errors, you will get the error infomation.

##### data

The return value from the method.

#### An example

https://innovaapi.aminer.cn/tools/v1/predict/career?per_name=XXX&org_name=XXX

Return Value:

```json
{
    "status": 0,
    "message": "success",
    "data": [
        {
            "name": "university of michigan",
            "p": 0.33
        },
        {
            "name": "university of california berkeley",
            "p": 0.33
        },
        {
            "name": "stanford university",
            "p": 0.33
        }
    ]
}
```

