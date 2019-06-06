'''
Introduction:
    Gender is a class which is used to predict a person's gender.
Usage:
>>> g = Gender()
>>> print(g.predict(name='Jie Tang', org='Tsinghua University', image_url='http://www.cs.tsinghua.edu.cn/publish/cs/4616/20110330101939787483549/20190321114128398502759.jpg'))
'''
import os
import json
import re
import pickle
import requests
from urllib.parse import quote_plus
from utils.crawler import baidu_parse, google_parse, getHTMLText
from config import model_path, api_key

data_path = os.path.join(model_path, 'gender')


class Gender:

    _face_url = 'https://api-us.faceplusplus.com/facepp/v3/detect'

    def __init__(self):
        self._name_model = json.load(open(os.path.join(data_path, 'model_name.json')))
        self._search_model = pickle.load(open(os.path.join(data_path, 'model_page.pk'), 'rb'), encoding='latin1')

    @staticmethod
    def get_firstname(name):
        # get first name from a full name
        try:
            name = name.lower()
            return name.split(' ')[0]
        except Exception:
            return ''

    @staticmethod
    def get_words(content):
        # get words from an article
        r = re.compile(r'[a-zA-Z]+|\.\.\.')
        words = re.findall(r, content)
        return [str(word.lower()) for word in words]

    def name_score(self, name):
        '''
        Predict a person's gender according to his or her name.
        :param name: The person's name
        :return: A dictionary:
                {
                    'male': probability that the person is male
                    'female': probability that the person is female
                }
        '''
        firstname = self.get_firstname(name)
        if firstname in self._name_model.keys():
            name_gender = self._name_model[firstname]
            return {
                'male': 1 if name_gender == 'male' else 0,
                'female': 1 if name_gender == 'female' else 0
            }
        else:
            return {
                'male': 0.5,
                'female': 0.5
            }

    def search_score(self, name, org, source='google'):
        '''
        Predict a person's gender using search engine.
        :param name: The person's name
        :param org: The person's organization
        :param source: Search engine, baidu or google
        :return: A dictionary:
                {
                    'male': Probability that the person is male,
                    'female': probability that the person is female
                }
        '''
        query = quote_plus('{} {} his OR her'.format(name, org))
        if source == 'baidu':
            url = 'https://www.baidu.com/s?wd={}&usm=1&tn=baidu&f=13&ie=utf-8&nojc=1&rqlang=en&rn=100'.format(query)
        elif source == 'google':
            url = 'https://www.google.com.hk/search?q={}&hl=en'.format(query)
        else:
            return {
                'male': 0.5,
                'female': 0.5
            }
        html = getHTMLText(url)
        if source == 'baidu':
            page_info = baidu_parse(html)
        else:
            page_info = google_parse(html)
        if not page_info:
            return {
                'male': 0.5,
                'female': 0.5
            }
        featureHis = self._get_feature('his', page_info, name)
        featureHer = self._get_feature('her', page_info, name)
        numSnippets = max(len(page_info), 1)
        tottf = max(float(featureHis['tf']+featureHer['tf']), 1.0)
        feature = [
            featureHis['tf']/tottf, featureHer['tf']/tottf,
            featureHis['df']/numSnippets, featureHer['tf']/numSnippets,
            int(featureHis['isNameInTitle']), int(featureHer['isNameInTitle']),
            int(featureHis['isInFirstSnippt']), int(featureHer['isInFirstSnippt'])
        ]
        # print(feature)
        mproba = self._search_model.predict_proba([feature])[0][1]
        return {
            'male': mproba,
            'female': 1 - mproba
        }

    def face_score(self, image_url=None, image_file=None):
        '''
        Predict a person's gender his or her photo.
        :param image_url: The photo's url
        :param image_file: The photo's local path
        :return: A dictionary:
                {
                    'male': Probability that the person is male,
                    'female': Probability that the person is female
                }
        '''
        try:
            data = {
                'api_key': api_key['api_key'],
                'api_secret': api_key['api_secret'],
                'return_landmark': '0',
                'return_attributes': 'gender'
            }
            if image_url is not None:
                data['image_url'] = image_url
                r = requests.post(Gender._face_url, data=data)
            elif image_file is not None:
                files = {'image_file': open(image_file, 'rb')}
                r = requests.post(Gender._face_url, data=data, files=files)
            else:
                return {
                    'male': 0.5,
                    'female': 0.5
                }
            # print(r.json())
            rdict = r.json()
            f = rdict.get('faces', [])[0]
            gender = f.get('attributes', {}).get('gender', {}).get('value')
            return {
                'male': 1 if gender == 'Male' else 0,
                'female': 1 if gender == 'Female' else 0
            }
        except Exception as ex:
            print(ex)
            return {
                'male': 0.5,
                'female': 0.5
            }
                
    def predict(self, name, org, source='google', image_url=None, image_file=None):
        '''
        Predict a person's gender.
        :param name: The person's name
        :param org: The person's organization
        :param source: Search engine, baidu or google
        :param image_url: The photo's url
        :param image_file: The photo's local path
        :return: A dictionary:
                {
                    'male': Probability that the person is male,
                    'female': Probability that the person is female,
                    'name': Probabilities from the person's name,
                    'search': Probabilities from search engine,
                    'face':  Probabilities from the person's photo
                }
        '''
        ret = {}
        weight = {
            'name': 1,
            'search': 1,
            'face': 1.1
        }
        ret['name'] = self.name_score(name)
        ret['search'] = self.search_score(name, org, source=source)
        ret['face'] = self.face_score(image_url, image_file)
        sum_p = 0
        male_v = 0
        for name, data in ret.items():
            if data['male'] != 0.5:
                male_v += data['male'] * weight[name]
                sum_p += weight[name]
        if sum_p > 0:
            male_p = male_v / sum_p
        else:
            male_p = 0.5
        ret['male'] = round(male_p, 2)
        ret['female'] = round(1 - male_p, 2)
        return ret

    def _get_feature(self, feature_name, page_info, name):
        # Extract some features about gender from the web page.
        feature = {
            'tf': 0,
            'df': 0,
            'isNameInTitle': False,
            'isInFirstSnippt': False
        }
        words_name = self.get_words(name)
        top3Snippets = []
        for pos, snippet in enumerate(page_info):
            words_title = self.get_words(snippet['title'])
            words_content = self.get_words(snippet['content'])
            if pos < 3:
                top3Snippets.extend(words_content)
            num = words_content.count(feature_name)
            if feature['isNameInTitle'] is False:
                if num > 0 and words_name[0] in words_title:
                    feature['isNameInTitle'] = True
            feature['tf'] += num
            if num > 0:
                feature['df'] += 1
        if feature_name in top3Snippets:
            feature['isInFirstSnippt'] = True
        return feature