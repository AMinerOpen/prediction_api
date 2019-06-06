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

