import requests


def youdao_translate(text):
    url = 'http://fanyi.youdao.com/translate'
    if type(text) == list:
        src = ','.join(text)
    else:
        src = text
    data = {
        'doctype': 'json',
        'type': 'EN2ZH_CN',
        'i': src,
    }
    rs = requests.get(url=url, params=data)
    try:
        trans_data = rs.json()['translateResult']
        tgt = [t['tgt'] for t in trans_data[0]]
        return tgt
    except Exception:
        # print('There is an error in translation')
        return []


if __name__ == '__main__':
    print(youdao_translate(['test','apple']))