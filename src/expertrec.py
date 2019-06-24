'''
Introduction:
    ExpertRec is a class which is used to recommend some experts in the given text's field.
Usage:
>>> e = ExpertRec()
>>> print(e.search('natural language processing'))
'''
import os
import fastText
import joblib
import json
import numpy as np
import heapq
from utils.acautomaton import ACAutomaton
from config import model_path

data_path = os.path.join(model_path, 'expert')


class ExpertRec:

    def __init__(self):
        self._model = fastText.load_model(os.path.join(data_path, 'model_aminer'))
        self._words = self._model.get_labels()
        self._index_mat = joblib.load(os.path.join(data_path, 'index_mat.pkl'))
        self._id2person = json.load(open(os.path.join(data_path, 'pid_list.json'), encoding='utf-8'))
        self.ac = ACAutomaton(self._words)
        self.base_url = 'http://www.aminer.cn/profile/{}'

    def doc2vec(self, text):
        # Convert text to vector.
        words = self.ac.search(text.lower().replace(' ', '_'))
        s = ' '.join([w.replace(' ', '_') for w in words])
        vec = self._model.get_sentence_vector(s)
        return vec

    def search(self, text, num=20):
        '''
        Recommend some experts in the given text's field.
        :param text: The text.
        :param num: The number of the recommended experts.
        :return: A list of dictionaries:
                {
                    'id': The expert's ID in AMiner(http://www.aminer.cn/),
                    'url': The expert's AMiner homepage.
                    'L2 distance': Similarity. The smaller the L2 distance is , the more likely the expert is interested in the given text's field.
                }
        '''
        vec = self.doc2vec(text)
        dist_mat = self._index_mat - vec.T
        dist = np.linalg.norm(dist_mat, axis=1)
        ret = [{
          'id': self._id2person[i],
          'url': self.base_url.format(self._id2person[i]),
          'L2 distance': d
        } for i, d in enumerate(dist)]
        return heapq.nsmallest(num, ret, lambda x: x['L2 distance'])


if __name__ == '__main__':
    e = ExpertRec()
    print(e.search('natural language processing'))