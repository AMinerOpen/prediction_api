# -*- coding: utf-8 -*-
'''
Introduction:
    AIClassifier is a class which is used to classify AI subjects.
    It depends on the classification of Natural Science Foundation of China(NSFC).
Usage:
    >>> ai_nsfc = AIClassifier()
    >>> words = ['search engine']
    >>> subject = ai_nsfc.classify(words)
'''
import os
from config import model_path
from sklearn.externals import joblib
from collections.abc import Iterable


data_path = os.path.join(model_path, 'nsfc')


class AIClassifier:

    def __init__(self, path=data_path):
        self._mat = []
        for level in range(3):
            file = os.path.join(path, 'ai_lev{}_w.pkl'.format(level))
            self._mat.append(joblib.load(file))

        file_id2name = os.path.join(path, 'id2name.pkl')
        file_id2father = os.path.join(path, 'id2father.pkl')
        self._id2name = joblib.load(file_id2name)
        self._id2father = joblib.load(file_id2father)

    def classify(self, words):
        '''
        Get the classification of the key words and its subject tree
        :param words: A key words list. Accept both English words and Chinese words
        :return:
                A dictionary contains four items:
                'level{x}'(x = 1, 2, 3): Related subjects of the words on level x.
                'tree': Subject trees of the given words(a list of dictionary).
        '''
        distribution = self._get_all_level_distribution(words)
        ret = self._get_all_info(words, distribution)
        subject_tree = self.get_tree(words, distribution)
        ret['tree'] = subject_tree
        return ret

    def get_tree(self, words, _distribution=None):
        '''
        Get a related subject tree using the key words
        :param words: A key words list. Accept both English words and Chinese words
        :param _distribution: A param designed to reuse codes.
        :return: Subject trees of the given words(a list of dictionary).
        '''
        subject_tree = {}
        if _distribution is None:
            _distribution = self._get_all_level_distribution(words)
        for level in range(0, 3):
            for k, p in _distribution[level].items():
                self._insert_subject2tree(k, p, subject_tree)
        return self._format_tree(subject_tree)

    def classify_level(self, words, level=1, lang_zh=False):
        '''
        Get the most likely subject names at the given level according to some key words
        :param words: A key words list. Accept both English words and Chinese words
        :param level: classification level(1, 2 or 3)
        :param zh: Whether to use Chinese subject names 
        :return: A list contains related subject names at the level
        '''
        if level not in [1, 2, 3]:
            return []
        main_subjects = self._get_all_level_distribution(words)
        if lang_zh:
            ret_iter = map(lambda x: self._get_zh_name(x), main_subjects[level - 1].keys())
        else:
            ret_iter = map(lambda x: self._get_name(x), main_subjects[level - 1].keys())
        return list(ret_iter)

    def _get_father_id(self, nsfc_id):
        return self._id2father.get(nsfc_id)

    def _get_name(self, nsfc_id):
        return self._id2name[nsfc_id][0]

    def _get_zh_name(self, nsfc_id):
        return self._id2name[nsfc_id][1]

    def _get_ancestors_list(self, nsfc_id):
        # get all of ancestors of a node on the subject tree
        ancestors = []
        father_id = self._get_father_id(nsfc_id)
        if father_id:
            ancestors.append(self._get_zh_name(father_id))
            # from top to bottom
            return self._get_ancestors_list(father_id) + ancestors
        else:
            return ancestors

    def _get_all_info(self, words, distribution=None):
        # Get the most likely subject names and their values at three levels
        ret = {}
        if distribution is None:
            distribution = self._get_all_level_distribution(words)
        for level in range(0, 3):
            level_name = 'level{}'.format(level + 1)
            ret[level_name] = []
            for k, p in distribution[level].items():
                ret[level_name].append({
                    'p': p,
                    'name': self._get_name(k),
                    'name_zh': self._get_zh_name(k)
                })
        return ret

    def _insert_subject2tree(self, nsfc_id, prob, tree):
        # insert a new node to a subject tree
        ancestors = self._get_ancestors_list(nsfc_id)
        point = tree
        node_name = self._get_zh_name(nsfc_id)
        if ancestors:
            for ancestor in ancestors:
                point = point.setdefault(ancestor, {'value': None})
                point = point.setdefault('child', {})
        point[node_name] = {'name': node_name, 'value': prob}

    def _get_all_level_distribution(self, words):
        restrict = None
        ret = []
        for i in range(0, 3):
            distri = self._get_distribution(words, i, restrict)
            main_subjects = self._get_main_subject(distri)
            ret.append(main_subjects)
            # ensure there is no repetition
            restrict = main_subjects.keys()
        return ret

    def _get_distribution(self, words, level, restrict=None, ban=None):
        # get the weight distribution at the given level
        rs = {}
        if words and isinstance(words, Iterable):
            for w in words:
                data = self._mat[level].get(w.lower(), {})
                for sub_id, v in data.items():
                    if ban is None or sub_id not in ban:
                        if restrict is None or self._id2father.get(sub_id) in restrict:
                            rs.setdefault(sub_id, 0)
                            rs[sub_id] += v
            self._norm(rs)
        return rs

    def _norm(self, dict_data):
        # normalize the value of a dictionary
        s = sum(dict_data.values())
        for k, v in dict_data.items():
            dict_data[k] = v / s

    def _format_tree(self, tree):
        '''
        In order to insert a node to a tree, we use subject names as keys.
        This function can format a subject tree(dictionary) by using the nodes itself as keys.
        '''
        new_tree = []
        for k, v in tree.items():
            child = v.get('child')
            if child:
                new_child = self._format_tree(child)
                new_tree.append({'name': k, 'value': v['value'], 'children': new_child})
            else:
                new_tree.append({'name': k, 'value': v['value']})
        return new_tree

    def _get_main_subject(self, distribution, thresh_prob=0.6, min_prob=0.1, dec_drop=10):
        # select the most possible subjects
        dis_len = len(distribution)
        if dis_len == 0:
            return {}
        sorted_distribution = sorted(distribution.items(), key=lambda x: -x[1])
        # after sorting, the dict becomes a list of pairs, item[0]: nsfc id, item[1]: its value
        ret = {sorted_distribution[0][0]: sorted_distribution[0][1]}
        sum_value = sorted_distribution[0][1]
        for i in range(1, dis_len):
            prev_value = sorted_distribution[i-1][1]
            now_value = sorted_distribution[i][1]
            if now_value < min_prob or (prev_value - now_value) / now_value > dec_drop:
                break
            ret[sorted_distribution[i][0]] = sorted_distribution[i][1]
            sum_value += now_value
            if sum_value > thresh_prob:
                break
        self._norm(ret)
        return ret

if __name__ == '__main__':
    words = [
        'Controlled Experiment',
        'Fit Tables.',
        'Executable Test Case',
        'Source Code',
        'Static Analysis',
        'Comprehension Task',
        'Legacy System',
        'Web Applications',
        'Genetic Algorithm',
        'Test Case',
        'Security Testing',
        'Empirical Study',
        'Acceptance Testing',
        'Data Model',
        'Fit Table',
        'Case Study',
        'Crosscutting Concern',
        'Web Application',
        'Empirical Studies',
        'Aspect Oriented Programming'
    ]
    aic = AIClassifier()
    print(aic.classify(words))