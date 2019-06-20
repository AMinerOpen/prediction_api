import sys
import json
import random
sys.path.append('../src')
from paperranker import PaperRanker
from baidu_translator import baidu_translate


pr = PaperRanker(use_clf=True)
with open('pageranker_test.json', 'r', encoding='utf-8') as f:
    s = f.read()
    correct = json.loads(s, encoding='utf-8')[0]['confirmed']
with open('542edff0dabfae498ae3c756.json', 'r', encoding='utf-8') as f:
    s = f.read()
    wrong = json.loads(s, encoding='utf-8')
random.shuffle(correct)
random.shuffle(wrong)
a = correct[0:40]
b = correct[40:] + wrong
ret, res = pr.label(a, b, threshold=0.5, trans=baidu_translate)
tp = 0
fp = 0
fn = 0
tn = 0
for item in ret:
    if item['flag'] == '1':
        tp += 1
    else:
        fp += 1
print(str(tp)+' '+str(fp))
for item in res:
    if item['flag'] == '1':
        fn += 1
    else:
        tn += 1
print(str(fn)+' '+str(tn))
