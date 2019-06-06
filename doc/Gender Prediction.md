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

Predict a person's gender.

#### Parameters

##### name

**string**, the person's name

##### org

**string**, the person's organization

##### source

Use `google` or `baidu` as the search engine

It is strongly recommended to use Google because the model is trained accoring to the results from Google.

##### image_url

The photo's url

#### An example

```python
g = Gender()
gen = g.predict(name='Jie Tang', org='Tsinghua University', image_url='http://www.cs.tsinghua.edu.cn/publish/cs/4616/20110330101939787483549/20190321114128398502759.jpg')
```

gen:

```python
{'name': {'male': 0.5, 'female': 0.5}, 'search': {'male': 0.9173952287088033, 'female': 0.0826047712911967}, 'face': {'male': 1, 'female': 0}, 'male': 0.96, 'female': 0.04}
```

