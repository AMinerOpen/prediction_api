'''
Introduction:
    JobHopping is a class which is used to predict where a scholar may hop to.
Usage:
>>> JobHopping.predict('tsinghua university')
'''
import pickle
import os
import torch
import torch.nn as nn
import heapq
import numpy as np
from libs import model_path

os.environ["CUDA_VISIBLE_DEVICES"] = '0'
data_path = os.path.join(model_path, 'jobhopping')


class GRUfn(nn.Sequential):
    # pytorch model
    def __init__(self, input_size, hidden_size, output_size):
        super(GRUfn, self).__init__()
        self.hidden_size = hidden_size
        self.input_size = input_size
        self.sig = nn.Sigmoid()
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
        self._affi = _model_data['affi_tensor']

        with open(os.path.join(data_path, 'orgID2orgname'), 'rb') as file:
            _data = pickle.load(file)
            for i, v in enumerate(_data):
                _id2name[i] = v.split('+')[0]
                _name2id.setdefault(v.split('+')[0],i)

        self._INPUT_DIM = 128
        self._OUTPUT_DIM = len(_id2name.keys())
        self._model = GRUfn(_INPUT_DIM, 512, _OUTPUT_DIM)
        self._model.load_state_dict(_model_data['state_dict'])

    def predict(self, name, ntop=3):
        '''
        get a scholar's possible future affiliation according to
        his current affiliation's name
        :param name: the scholar's affiliation name
        :param ntop: How many possible affiliations will the method return
        :return: A list of dictionary:
                {
                    'name': the most likely future affiliation's name
                    'p': the probability
                }
        '''
        name = name.lower()
        if name not in self._name2id.keys():
            return None
        zb = self.id2PackedSequence(self._name2id[name])
        fout = self._model(zb, batch=1)
        ans = heapq.nlargest(ntop, enumerate(fout.data.numpy()[0]), key=lambda x:x[1])
        ret = []
        for id, p in ans:
            ret.append({
                'name': self._id2name[id],
                'p': p,
            })
        self._softmax(ret)
        return ret

    def id2PackedSequence(self, affi_id):
        # In pytorch, all RNN modules accept packed sequences as inputs.
        ret = torch.zeros(1, 1, self._INPUT_DIM)
        indices = torch.tensor(affi_id, device='cpu', dtype=torch.long)
        ret[0] = torch.index_select(self._affi, 0, indices)
        return torch.nn.utils.rnn.pack_padded_sequence(ret, [1])

    def _softmax(self, affis):
        '''
        Softmax is a generalization of logistic function that "squashes"(maps) a vector of arbitrary real values
        to a vector of real values in the range (0, 1) that add up to 1.
        '''
        s = sum(map(lambda x: np.exp(x['p']), affis))
        for dict in affis:
            dict['p'] = round(np.exp(dict['p'])/s, 2)
