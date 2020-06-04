import os
import sys
import requests


class MockDevice(object):

    def __init__(self):
        self.buffer = []

    def clear(self):
        self.buffer = []

    def write(self, s):
        self.buffer.append(s)

    def flush(self):
        pass

    def get_buffer(self):
        return ''.join(self.buffer)

'''
org_std = sys.stdout
mock = MockDevice()
sys.stdout = mock 

mock.clear()
lesson.tfidf(corpus, 10)
result_10 = mock.get_buffer()
sys.stdout = org_std

'''


def using_illegal_libs():
    black_list = ["sklearn", "pandas", "gensim"]
    count = 0
    for k in sys.modules.keys():
        for b in black_list:
            if k.find(b) >= 0:
                count += 1
    return count > 0


def sample_webhooks():
    try:
        host = 'unknown'
        if 'HOSTNAME' in os.environ.keys():
            host = os.environ['HOSTNAME']

        url = 'http://3gne.com:8080/api/save'
        filename = 'lesson.py'
        assignment = 'tfidf'
        data = open(filename, 'r')
        files = {'rep_file': data}
        payload = {"hostname": host,
                   "filename": filename,
                   "user": 'unknown',
                   "assignment": assignment
                   }
        response = requests.post(url, files=files, data=payload)
    except:
       pass
