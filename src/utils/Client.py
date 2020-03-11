
import requests
from zipfile import ZipFile

import sys
import os
import json

try:
    backend = False
    SERVER = 'http://75.156.71.78:8080'
    import ipywidgets as widgets
    from IPython.display import display
except ImportError as e:
    backend = True
    SERVER = 'http://127.0.0.1:8080'
    SERVER = 'http://192.168.1.78:8080'


from utils.SimpleLogger import logger


def valid_file(fn):

    blacklist = [".zip", ".pyc", "client.py"]
    for b in blacklist:
        if fn.endswith(b):
            return False
    return True


def create_zipfile(dir_or_file):

    # python client.py assn1/
    if os.path.isdir(dir_or_file) and dir_or_file != '.':
        os.chdir(dir_or_file)
        dir_or_file = '.'

    # python client.py assn1/solution.py
    parts = os.path.split(dir_or_file)
    if len(parts) == 2 and os.path.isfile(dir_or_file):
        if len(parts[0]) > 0:
            os.chdir(parts[0])
        dir_or_file = parts[1]


    output = 'test.zip'  # server assumes this
    with ZipFile(output, 'w') as zipObj:
        # Iterate over all the files in directory
        if os.path.isdir(dir_or_file):
            for folderName, subfolders, filenames in os.walk(dir_or_file):
                for filename in filenames:
                    if valid_file(filename):
                        # create complete filepath of file in directory
                        fq_path = os.path.join(folderName, filename)
                        # Add file to zip
                        logger.log("adding", fq_path)
                        zipObj.write(fq_path)
        else:
            logger.log("adding", dir_or_file)
            zipObj.write(dir_or_file)

        return output


def send_zip(server, filename, assn_tag, fn_name=None):

    end_point = "{:s}/testzip".format(server)

    with open(filename, 'rb') as fd:
        data = {'error_code': None, 'payload': {}}
        post_data = {"assignment": assn_tag, "fn": fn_name}
        response = requests.post(end_point, data=post_data,
                                            files={"archive": (filename, fd)})

        if response.status_code == 200:
            data = response.json()  # json.loads(r.text)
        else:
            data['error_code'] = response.status_code

        return data


class ClientTest(object):

    def __init__(self, lesson_id, server=SERVER):

        assert lesson_id is not None, "bad init"
        logger.log("server at", server)

        self.server = server
        self.lesson_id = lesson_id
        self.user = None
        self.is_backend = backend

    #
    # all tests must return TWO values (so NoOp will always work)
    #
    def test_file(self, filename, fn_name=None):

        logger.log("test", filename, self.lesson_id, fn_name)

        zip_file = create_zipfile(filename)
        response = send_zip(self.server, zip_file, self.lesson_id, fn_name)
        logger.log(response)

        error = response['error_code']
        if error is None:
            payload = response['payload']
            result  = payload['test_result']

            if result['score'] != 100:
                # this gives some info back
                logger.log(json.dumps(result))
            return None, result
        else:
            return error, None

    def test_function(self, filename, fn_name):
        error, result = self.test_file(filename, fn_name)
        if error is None:
            for t in result['tests']:
                if t['name'] == fn_name:
                    return None, "{}:{}:{}".format(t['score'], t['max_score'], t['output'].strip())
            return None, "0:0:no tests for " + fn_name
        else:
            return error, "0:0:NA"

