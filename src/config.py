import os
# The directory of models
src_path = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(src_path)
model_path = os.path.join(base_path, 'model')
'''
Please put your api key here
You can know how to get it in https://console.faceplusplus.com/documents/7079083.
api_key = {
    'api_key': '',
    'api_secret': ''
}
'''
api_key = None
