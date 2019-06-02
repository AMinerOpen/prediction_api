import os
import json
import re
import pickle
from utils.crawler import baidu_parse, google_parse, getHTMLText
from config import model_path

data_path = os.path.join(model_path, 'gender')


class Gender:

    SEARCH_THRESHOLD = 0.59

    def __init__(self):
        self._name_model = json.load(open(os.path.join(data_path, 'model_name.json')))
        self._search_model = pickle.load(open(os.path.join(data_path, 'model_page.pk'), 'rb'), encoding='latin1')

    @staticmethod
    def get_firstname(name):
        try:
            name = name.lower()
            return name.split(' ')[0]
        except Exception:
            return ''

    @staticmethod
    def get_words(content):
        r = re.compile(r'[a-zA-Z]+|\.\.\.')
        words = re.findall(r, content)
        return [str(word.lower()) for word in words]

    def name_score(self, name):
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

    def search_score(self, name, org, source='baidu'):
        query = '{} {} his OR her'.format(name, org)
        if source == 'baidu':
            url = 'https://www.baidu.com/s?wd={}&usm=1&tn=baidu&f=13&ie=utf-8&nojc=1&rqlang=en'.format(query)
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
        print(feature)
        mproba = self._search_model.predict_proba([feature])[0][1]
        return {
            'male': mproba,
            'female': 1 - mproba
        }

    def _get_feature(self, feature_name, page_info, name):
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



if __name__ == "__main__":
    g = Gender()
    print(g.search_score('Jie Tang', 'Tsinghua University', source='google'))
