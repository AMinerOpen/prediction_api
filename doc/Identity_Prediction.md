# Identity Prediction

## Introduction

Predict a scholar's identity (teacher or student) and his or her degree.

## Method

### predict

```python
predict(pc=0, cn=0, hi=0, gi=0, year_range=0)
```

#### Introduction

Predict whether a scholar is a teacher or a student, and then predict his degree.

#### Parameters

##### pc

Number of papers

##### cn

Citation number

##### hi

H-index. Eg, an h-index of 25 means the researcher has 25 papers, each of which has been cited 25+ times.

##### gi

G-index. Given a set of articles ranked in decreasing order of the number of citations that they received, the g-index is the (unique) largest number such that the top g articles received (together) at least g^2 citations.

##### year_range

Time range of papers.

#### Return value

A dictionary:

```python
{
    'label': 'student' or 'teacher',
    'degree': 'undergraduate', 'master' or 'doctor'
    'p': probability
}
```

#### An example

```python
identity = TorS()
i = identity.predict(pc=10, cn=10000, hi=40, gi=0, year_range=14)
```

`i`:

```python
{'label': 'teacher', 'degree': 'doctor', 'p': 0.9993}
```

## API

### https://innovaapi.aminer.cn/tools/v1/predict/identity

![](https://img.shields.io/badge/http-get-brightgreen.svg)

An online version of the method `predict`

#### Parameters

##### pc

Number of papers

##### cn

Citation number

##### hi

H-index. Eg, an h-index of 25 means the researcher has 25 papers, each of which has been cited 25+ times.

##### gi

G-index. Given a set of articles ranked in decreasing order of the number of citations that they received, the g-index is the (unique) largest number such that the top g articles received (together) at least g^2 citations.

##### year_range

Time range of papers.

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

https://innovaapi.aminer.cn/tools/v1/predict/identity?pc=10&cn=10000&hi=40&gi=0&year_range=14

`Response`:

```json
{
    "status": 0,
    "message": "success",
    "data": {
        "label": "teacher",
        "degree": "doctor",
        "p": 0.9993
    }
}
```

