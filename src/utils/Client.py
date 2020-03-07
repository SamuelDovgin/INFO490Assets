
import requests
import os
import json
from zipfile import ZipFile



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
                        print("adding", fq_path)
                        zipObj.write(fq_path)
        else:
            print("adding", dir_or_file)
            zipObj.write(dir_or_file)

        return output


def send_zip(server, filename, assn_tag):

    with open(filename, 'rb') as fd:
        data = {'error_code': None, 'payload': {}}
        r = requests.post(server,
                          data={"assignment": assn_tag},
                          files={"archive": (filename, fd)})

        if r.status_code == 200:
            data = json.loads(r.text)
        else:
            data['error_code'] = r.status_code

        return data


class ClientTest(object):

    def __init__(self, server, user, lesson_id):
        self.server = server
        self.user = user
        self.lesson_id = lesson_id

    def test_file(self, filename):

        zip_file = create_zipfile(filename)
        response = send_zip(self.server, zip_file, self.lesson_id)

        error = response['error_code']
        payload = response['payload']
        if error is None:
            print(json.loads(payload['test_result']))
        else:
            print('ERROR', error)

