'''
Introduction:
    JobHopping is a class which is used to predict where a scholar may hop to.
Usage:
>>> j = JobHopping()
>>> print(j.predict('tsinghua university'))
'''
import pickle
import os
import torch
import torch.nn as nn
import heapq
import numpy as np
from prediction_api.src.config import model_path
import torch.nn.functional as F

os.environ["CUDA_VISIBLE_DEVICES"] = '0'
data_path = os.path.join(model_path, 'jobhopping')


class GRUfn(nn.Sequential):

    def __init__(self, input_size, hidden_size, output_size):
        super(GRUfn, self).__init__()
        self.hidden_size = hidden_size
        self.input_size = input_size
        self.sig    = nn.Sigmoid()
        self.cr = nn.GRU(input_size=input_size, hidden_size=hidden_size)
        self.fn = nn.Linear(hidden_size, output_size)
        self.fn2 = nn.Linear(hidden_size, output_size)

    def forward(self, x, y=None, batch=256):
        if y is not None:
            x, y = self.cr(x, y)
        else:
            x, y = self.cr(x)
        x = torch.nn.utils.rnn.pad_packed_sequence(x)
        r = torch.transpose(x[0], 0, 1)
        y = y.view(batch, self.hidden_size)
        ind = x[1].view(batch, 1, 1)
        ind = ind - 1
        ind = ind.expand(-1, -1, self.hidden_size)
        t = torch.gather(r, 1, ind)
        t = t.view(batch, self.hidden_size)
        t = self.fn(t)
        y = self.fn2(y)
        t = t + y
        t = self.sig(t)
        return t


class JobHopping:

    def __init__(self):
        self._id2name = {}
        self._name2id = {}
        self._model_data = torch.load(os.path.join(data_path, 'model'))
        self._affi = self._model_data['affi_tensor']

        with open(os.path.join(data_path, 'orgID2orgname'), 'rb') as file:
            _data = pickle.load(file)
            for i, v in enumerate(_data):
                self._id2name[i] = v.split('+')[0]
                self._name2id.setdefault(v.split('+')[0], i)

        self._INPUT_DIM = 128
        self._OUTPUT_DIM = len(self._id2name.keys())
        self._model = GRUfn(self._INPUT_DIM, 512, self._OUTPUT_DIM)
        self._model.load_state_dict(self._model_data['state_dict'])

    def predict(self, name_squence, ntop=3):
        '''
        get a scholar's possible future affiliation according to
        his current affiliation's name
        :param name: the scholar's affiliation name
        :param ntop: How many possible affiliations will the method return
        :return: A list of dictionaries:
                {
                    'name': the most likely future affiliation's name
                    'p': the probability
                }
        '''

        name_squence = [x.lower() for x in name_squence]
        name2id_squence = [self._name2id[name] for name in name_squence if name in self._name2id.keys()]
        # if len(name_squence) != len(name2id_squence):
        #     return None
        temp_squence = name2id_squence
        name2id_squence = []
        if len(temp_squence) != 0:
            name2id_squence.append(temp_squence[0])
            [name2id_squence.append(term) for index, term in enumerate(temp_squence) if index != 0 and term != temp_squence[index - 1]]
        else:
            return None
        # 去掉重复环路
        name2id_squence = self._delete_ring(name2id_squence)
        zb = self._id2PackedSequence(name2id_squence)
        fout = self._model(zb, batch=1)
        # softmax_fout = F.softmax(fout,1)
        # ans = heapq.nlargest(ntop, enumerate(softmax_fout.data.numpy()[0]), key=lambda x:x[1])
        ans = heapq.nlargest(ntop, enumerate(fout.data.numpy()[0]), key=lambda x:x[1])
        ret = []
        for id, p in ans:
            ret.append({
                'name': self._id2name[id],
                'p': p,
            })
        self._softmax(ret)
        return ret
    def _delete_ring(self,id_squence):
        clear_squence = id_squence
        itmes = 1000
        while True:
            res = self._getNumofCommonSubstr(clear_squence, clear_squence)
            if res[1] < 2:
                break
            a = "_".join([str(ss) for ss in res[0]])
            b = "_".join([str(ss) for ss in clear_squence])
            temp = b
            times = 1000
            while times > 1:
                if b.rfind(a) != -1:
                    temp = b
                    b = self._rreplace(b, a, "_", 1)
                    times -= 1
                else:
                    break
            clear_squence = [int(term) for term in temp.split("_") if term != ""]
            # id_squence = [int(s) for s in clear_squence]
        # clear_squence = id_squence
        return clear_squence

    def _getNumofCommonSubstr(self,str1, str2):
        lstr1 = len(str1)
        lstr2 = len(str2)
        record = [[0 for i in range(lstr2 + 1)] for j in range(lstr1 + 1)]  # 多一位
        maxNum = 0  # 最长匹配长度
        p = 0  # 匹配的起始位

        for i in range(lstr1):
            for j in range(lstr2):
                if str1[i] == str2[j] and abs(i - j) > maxNum:
                    # 相同则累加
                    record[i + 1][j + 1] = record[i][j] + 1
                    if record[i + 1][j + 1] > maxNum:
                        # 获取最大匹配长度
                        maxNum = record[i + 1][j + 1]
                        # 记录最大匹配长度的终止位置
                        p = i + 1
        # return p - maxNum,p, maxNum
        return str1[p - maxNum:p], maxNum

    def _rreplace(self,st, old, new, *max):
        count = len(st)
        if max and str(max[0]).isdigit():
            count = max[0]
        return new.join(st.rsplit(old, count))

    def _id2PackedSequence(self, affi_id):
        # 输入的形状可以是 (T×B×*)。T 是最长序列长度，B 是 batch size，* 代表任意维度 (可以是 0)。如果 batch_first=True 的话，那么相应的 input size 就是 (B×T×*)。
        ret = torch.zeros(1, len(affi_id), self._INPUT_DIM)
        indices = torch.tensor(affi_id, device='cpu', dtype=torch.long)
        ret[0] = torch.index_select(self._affi, 0, indices)
        return torch.nn.utils.rnn.pack_padded_sequence(ret, [len(affi_id)],batch_first=True)

    def _softmax(self, affis):
        # Softmax is a generalization of logistic function that "squashes"(maps) a vector of arbitrary real values to a vector of real values in the range (0, 1) that add up to 1.
        s = sum(map(lambda x: np.exp(x['p']), affis))
        for dict in affis:
            dict['p'] = round(np.exp(dict['p'])/s, 2)