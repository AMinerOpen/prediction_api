'''
Introduction:
    Predict a scholar's identity (teacher or student) and his or her degree.
usage:
>>> identity = TorS()
>>> print(identity.predict(pc=10, cn=10000, hi=40, gi=0, year_range=14))
'''
import os
import math
import json
import numpy as np
import tensorflow as tf
import pandas as pd
from config import model_path

data_path = os.path.join(model_path, 'student')


class TorS:

    def __init__(self):
        self.feature_cols = [tf.feature_column.numeric_column(f) for f in ['pc', 'cn', 'hi', 'gi', 'year_range']]
        self._md = tf.estimator.DNNClassifier(
            hidden_units=[10, 10],
            feature_columns=self.feature_cols,
            model_dir=data_path,
        )

    def predict(self, pc=0, cn=0, hi=0, gi=0, year_range=0):
        '''
        Predict whether a scholar is a teacher or a student, and then predict his degree.
        :param pc: Number of papers
        :param cn: Citation number
        :param hi: H-index. Eg, an h-index of 25 means the researcher has 25 papers, each of which has been cited 25+ times.
        :param gi: G-index. Given a set of articles ranked in decreasing order of the number of citations that they received,
                   the g-index is the (unique) largest number such that the top g articles received (together) at least g^2 citations.
        :param year_range: Time range of papers
        :return: A dictionary:
                {
                    'label': 'student' or 'teacher',
                    'degree': 'undergraduate', 'master' or 'doctor'
                    'p': probability
                }
        '''
        features = dict(pc=pc, cn=cn, hi=hi, gi=gi, year_range=year_range)
        input = pd.read_json(json.dumps([features]))
        output = self._md.predict(input_fn=lambda: self._pre_progress(input))
        ans = [(int(item['class_ids'][0]), item['probabilities'][item['class_ids'][0]]) for item in output][0]
        label = 'student' if ans[0] == 1 else 'teacher'
        if label == 'teacher':
            degree = 'doctor'
        else:
            degree = 'master' if pc >= 2 else 'undergraduate'
        ret = {
            'label': label,
            'degree': degree,
            'p': round(float(ans[1]), 4)
        }
        return ret

    def _pre_progress(self, features):
        # Normalize and pass features to nn classifier for prediction
        max_year_range = 53  # 53 is the max year_range in training set.
        normalized_features = pd.DataFrame()
        for feature in ['pc', 'cn', 'hi', 'gi']:
            normalized_features[feature] = features[feature].apply(lambda x: math.log(x + 1.0))
        normalized_features['year_range'] = features['year_range'].apply(lambda x: x / max_year_range)
        ret = {key: np.array(value) for key, value in dict(normalized_features).items()}
        ds = tf.data.Dataset.from_tensor_slices(ret)
        ds = ds.batch(1).repeat(1)
        ret = ds.make_one_shot_iterator().get_next()
        return ret
