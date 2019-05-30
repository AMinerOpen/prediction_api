import os
import json
from scrapy.selector import Selector
import re

from config import model_path

data_path = os.path.join(model_path, 'gender')


class Gender:

    def __init__(self):
        self._name_model = json.load(open(os.path.join(data_path, 'model_name.json')))

    @classmethod
    def get_firstname(cls, name):
        try:
            name = name.lower()
            return name.split(' ')[0]
        except Exception:
            return ''

    def name_score(self, name):
        firstname = Gender.get_firstname(name)
        if firstname in self._name_model.keys():
            name_gender = self._name_model[firstname]
            print(firstname)
            return {
                'male': 1 if name_gender == 'male' else 0,
                'female': 1 if name_gender == 'female' else 0
            }
        else:
            return {
                'male': 0.5,
                'female': 0.5
            }

    @classmethod
    def google_parser(cls, text):
        page = Selector(text=text)
        rs = []
        for ans in page.css('div.g'):
            title = ''.join(ans.css('h3').css('*::text').extract())
            content = ''.join(ans.css('span.st').css('*::text').extract())
            url = ans.css('*.r a::attr(href)').extract()
            try:
                url = re.findall('(http.*)', url[0])
                url = re.sub('&.*', '', url[0])
                rs.append({
                    'url': url,
                    'content': content,
                    'title': title,
                })
            except Exception:
                pass
        return rs

if __name__ == "__main__":
    with open(os.path.join(data_path, 'test.html')) as f:
        text = f.read()
        print(Gender.google_parser(text))