'''
Introduction:
PaperRanker is a class which is used to predict how much possibility there is that a publication is belong to a professor.
Usage:
>>> ret, res = pr.label(a, b, threshold=0.5)
'''
from classifier import Classifier
from Levenshtein import jaro_winkler
from utils.translator import youdao_translate
import copy
import time


class PaperRanker:

    def __init__(self, use_clf=False):
        self.clf = Classifier()
        self.use_clf = use_clf
        self.weight = {
           'coauthor_score': 0.7 if use_clf else 0.9,
           'pubyear_score': 0.1,
        }
        if use_clf:
            self.weight['field_score'] = 0.2
        print(self.weight)

    def ranking(self, correct_pubs, unsure_pubs, threshold=0.5, trans=youdao_translate):
        '''
        Predict how much possibility there is that a publication is belong to a professor.
        :param correct_pubs: A list of this professor's publications.
        :param unsure_pubs: A list of unsure publications
        :param threshold: If the possibility of a publication is smaller than this threshold, it won't consider as a correct publication.
        :param trans: In fact, the classifier can only work on Chinese words because of the classification standard and the training data. In order to handle publications in other languages, you need to provide a translation function.  It should be able to translate a list of strings in another language to Chinese.
        :return: (a,b), two list of unsure publications and their possibilities. The first one has high possibilities, and the second one has low possibilities. 
        '''
        ret = copy.deepcopy(unsure_pubs)
        ret = self.coauthor_score(correct_pubs, ret)
        if self.use_clf:
            ret = self.field_score(correct_pubs, ret, trans=trans)
        ret = self.pubyear_score(ret)
        for pub in ret:
            pub['score'] = 0
            for name, weight in self.weight.items():
                pub['score'] += pub[name] * weight
        res = [pub for pub in ret if pub['score'] < threshold]
        ret = [pub for pub in ret if pub['score'] >= threshold]
        sorted(ret, key=lambda x: x['score'], reverse=True)
        sorted(res, key=lambda x: x['score'], reverse=True)
        return ret, res

    def label(self, correct_pubs, unsure_pubs, threshold=0.5, trans=youdao_translate):
        '''
        Use iterative algorithm to predict how much possibility there is that a publication is belong to a professor.
        :param correct_pubs: A list of this professor's publications.
        :param unsure_pubs: A list of unsure publications
        :param threshold: If the possibility of a publication is smaller than this threshold, it won't consider as a correct publication.
        :param trans: In fact, the classifier can only work on Chinese words because of the classification standard and the training data. In order to handle publications in other languages, you need to provide a translation function.  It should be able to translate a list of strings in another language to Chinese.
        :return: (a,b), two list of unsure publications and their possibilities. The first one has high possibilities, and the second one has low possibilities. 
        '''
        co = []
        uns = copy.deepcopy(unsure_pubs)
        cnt = 1
        while True:
            print('round {}'.format(cnt))
            cnt += 1
            ret, res = self.ranking(co + correct_pubs, uns, threshold, trans=trans)
            co = co + ret
            uns = res
            if len(ret) == 0:
                break
            time.sleep(4)
        return co, uns

    def coauthor_score(self, correct_pubs, unsure_pubs):
        authors = set()
        for pub in correct_pubs:
            authors = authors.union(set(pub['authors']))
        for pub in unsure_pubs:
            num = 0
            for name_b in pub['authors']:
                score = 0
                for name_a in authors:
                    score = max(score, self.name_match(name_a, name_b))
                num += score
            if len(pub['authors']) == 0:
                pub['coauthor_score'] = 0
            else:
                pub['coauthor_score'] = min(1.0, max(num/len(pub['authors']), num*0.12))
        return unsure_pubs

    def field_score(self, correct_pubs, unsure_pubs, trans=youdao_translate):
        titles = list(map(lambda x: x['title'], correct_pubs))
        distribution = self.clf.classify(pub_titles=titles, level=1, ntop=5, translatation_func=trans)
        codes = set(map(lambda x: x['code'], distribution['level1']))
        cnt = 0
        for pub in unsure_pubs:
            cnt += 1
            now_dist = self.clf.classify(pub_titles=[pub['title']], level=1, ntop=5, translatation_func=trans)
            if now_dist:
                intersect = set(map(lambda x: x['code'], now_dist['level1']))&codes
            else:
                intersect = []
            pub['field_score'] = len(intersect)/5
        return unsure_pubs

    def pubyear_score(self, unsure_pubs):
        for pub in unsure_pubs:
            if pub['year']:
                year = int(pub['year'])
                pub['pubyear_score'] = min(1.0, (year - 1950) / (2019 - 1950))
            else:
                pub['pubyear_score'] = 0.5
        return unsure_pubs

    def name_match(self, name_a, name_b):
        '''
        For example, we cannot totally assert Professor 'J. Tang' and Professor 'Jie Tang' are the same person.
        We use this function to estimate how much possibility that two professors' name belong to one person.
        '''
        name_a = name_a.lower().strip().replace('.', '').replace('-', '').replace(u'\xa0', '')
        name_b = name_b.lower().strip().replace('.', '').replace('-', '')
        if name_a == name_b:
            return 1
        elif name_a[0] != name_b[0]:
            return 0
        lastname_a = name_a.split(' ')[-1]
        lastname_b = name_b.split(' ')[-1]
        if lastname_a != lastname_b:
            return 0
        firstname_a = name_a.split(' ')[0]
        firstname_b = name_b.split(' ')[0]
        if len(firstname_a) != 1 and len(firstname_b) != 1:
            return 0
        return jaro_winkler(name_a, name_b)