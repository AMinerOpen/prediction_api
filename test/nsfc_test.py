import sys
import json
sys.path.append('../src')
from classifier import Classifier

clf = Classifier()
f = open('nsfc_test.json', 'r', encoding='utf-8')
s = f.read()
j = json.loads(s, encoding='utf-8')
data = j['nsfc']
for level in [1, 2, 3]:
    cnt = 0
    top1 = 0
    top5 = 0
    length = level * 2 + 1
    for item in data:
        if len(item['sid']) < length:
            continue
        subject = clf.classify([item['title']], level=level, lang_zh=True)
        if subject == {}:
            continue
        cnt += 1
        if subject['level{}'.format(level)][0]['code'] == item['sid'][0:length]:
            top1 += 1
        for ret in subject['level{}'.format(level)]:
            if ret['code'] == item['sid'][0:length]:
                top5 += 1
                break
    print('level', level, ':', top1/cnt, ' ', top5/cnt, ' ', cnt)
        