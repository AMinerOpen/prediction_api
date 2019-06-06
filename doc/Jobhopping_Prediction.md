# Jobhopping Prediction

## Introduction

JobHopping is a class which is used to predict where a scholar may hop to.

## Method

### predict

```python
predict(name, ntop=3)
```

#### Introduction

Get a scholar's possible future affiliation according to his current affiliation's name.

#### Parameters

##### name

The scholar's affiliation name

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
aff = j.predict('tsinghua university')
```

`aff`:

```python
[
    {
        'name': 'university of michigan',
        'p': 0.33
    }, 
    {
        'name': 'university of california berkeley',
        'p': 0.33
    }, 
    {
        'name': 'stanford university',
        'p': 0.33
    }
]
```

## API

### https://innovaapi.aminer.cn/tools/v1/predict/career

![](https://img.shields.io/badge/http-get-brightgreen.svg)

An online version of method `predict`

#### Parameters

##### org

The scholar's affiliation name

#### An example

https://innovaapi.aminer.cn/tools/v1/predict/career?org=Tsinghua%20University

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

