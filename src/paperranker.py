from classifier import Classifier
from Levenshtein import jaro_winkler
import copy


class PaperRanker:

    def __init__(self):
        self.clf = Classifier()
        self.weight = {
           'coauthor_score': 0.7,
           'field_score': 0.2,
           'pubyear_score': 0.1,
        }

    def ranking(self, correct_pubs, unsure_pubs, threshold=0):
        '''
        Predict how much possibility there is that a publication is belong to a professor.
        :param correct_pubs: A list of this professor's publications.
        :param unsure_pubs: A list of unsure publications
        :param threshold: If the possibility of a publication is smaller than this threshold,
                          it won't exist in the return value.
        :return: The list of unsure publications and their possibilities.
        '''
        ret = copy.deepcopy(unsure_pubs)
        self.coauthor_score(correct_pubs, ret)
        self.field_score(correct_pubs, ret)
        self.pubyear_score(ret)
        for pub in unsure_pubs:
            pub['score'] = 0
            for name, weight in self.weight:
                pub['score'] += pub[name] * weight
        ret = [pub for pub in ret if pub['score'] > threshold]
        list.sort(ret, reverse=True)
        return ret

    def coauthor_score(self, correct_pubs, unsure_pubs):
        authors = set()
        for pub in correct_pubs:
            authors = authors.union(set(pub))
        for pub in unsure_pubs:
            score = 0
            for name_a in authors:
                for name_b in pub['authors']:
                    score = max(score, self.name_match(name_a, name_b))
            pub['coauthor_score'] = score

    def field_score(self, correct_pubs, unsure_pubs):
        titles = list(map(lambda x: x['title'], correct_pubs))
        distribution = self.clf.classify(pub_titles=titles, level=1, ntop=5)
        codes = set(map(lambda x: x['code'], distribution))
        for pub in unsure_pubs:
            now_dist = self.clf.classify(pub_titles=[pub['title']], level=1, ntop=5)
            intersect = set(map(lambda x: x['code'], now_dist)) & codes
            pub['field_score'] = len(intersect)/5

    def pubyear_score(self, unsure_pubs):
        for pub in unsure_pubs:
            if pub['year']:
                year = int(pub['year'])
                pub['pubyear_score'] = min(1.0, (year - 1950) / (2019 - 1950))
            else:
                pub['pubyear_score'] = 0.5

    def name_match(self, name_a, name_b):
        '''
        For example, we cannot totally assert Professor 'J. Tang' and Professor 'Jie Tang' are the same person.
        We use this function to estimate how much possibility that two professors' name belong to one person.
        '''
        name_a = name_a.lower().strip().replace('.', '').replace('-', '')
        name_b = name_b.lower().strip().replace('.', '').replace('-', '')
        if name_a == name_b:
            return 1
        elif name_a[0] != name_b[0]:
            return 0
        lastname_a = name_a.split(' ')[-1]
        lastname_b = name_b.split(' ')[-1]
        if lastname_a != lastname_b:
            return 0
        return jaro_winkler(name_a, name_b)


if __name__ == '__main__':
    pr = PaperRanker()
    