
import requests
from zipfile import ZipFile

import sys
import os

try:
    backend = False
    SERVER = 'http://75.156.71.78:8080'
    import ipywidgets as widgets
    from IPython.display import display
except ImportError as e:
    backend = True
    SERVER = 'http://127.0.0.1:8080'
    SERVER = 'http://192.168.1.78:8080'


sys.path.append('..')
from utils.Tools import logger


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
        self.backend = backend

    def test_file(self, filename, fn_name=None):

        logger.log("test", filename, self.lesson_id, fn_name)

        zip_file = create_zipfile(filename)
        response = send_zip(self.server, zip_file, self.lesson_id, fn_name)

        error = response['error_code']
        if error is None:
            payload = response['payload']
            result  = payload['test_result']
            if result['score'] == 0:

                # this gives some info back
                print(result)

                ''' 
                could loop through all the tests
                looking at 'output' filed
                and make sense of the error
                import re
                p = r'File *solution.py'
                m = re.search(p, payload['stdout'])
                print("SEATVH", payload['stdout'])
                if m is not None:
                    print(m)
                else:
                   print(error)
                   print(payload)
                '''

            return result
        else:
            return error

    def test_function(self, filename, fn_name):
        result = self.test_file(filename, fn_name)
        for t in result['tests']:
            if t['name'] == fn_name:
                return t['score'], t['max_score']
        return 0, 0

