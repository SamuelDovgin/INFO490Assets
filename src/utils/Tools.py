
'''

# This module allows for testing colab code
# while debugging and testing, need to reload the module
import importlib
importlib.reload(Tools)

from info490.src.utils import Tools as helper
print(dir(tester))

'''

import sys
import json
import urllib.parse
import urllib.request
import requests
from datetime import datetime
import time

class SimpleLogger(object):
    def __init__(self):
        self.logger = open("debug_log.txt", "w")

    def log(self, *args):
        to_write = " ".join([str(a) for a in args])
        self.logger.write(to_write + '\n')
        self.logger.flush()
logger = SimpleLogger()

def install_gd_file(doc_id, filename, force=False, persist=True):

    #import importlib
    if not force and os.path.exists(filename):
        logger.log("reading cached version")
        with open(filename, 'r') as fd:
           return fd.read()

    baseurl = "https://drive.google.com/uc"
    params = {"export": "download", "id": doc_id}

    url = baseurl + "?" + urllib.parse.urlencode(params)
    try:

        #resp = requests.head(url)
        #print(resp.status_code, resp.text, resp.headers)

        r = urllib.request.urlopen(url)
        #print('DATE', r.headers['last-modified'])
        #print('DATE', r.headers)

        text = str(r.read().decode('UTF-8'))
        if persist:
            with open(filename, 'w') as fd:
                 fd.write(text)
        return text
    except Exception as e:
        print("unable to load notebook at", url, str(e))
        return None



class TestFramework(object):

    JSON_FILE    = 'solution.json'
    STUDENT_FILE = 'solution.py'

    def __init__(self, notebook_id, client):

        assert notebook_id is not None, "bad init"

        self.notebook_id = notebook_id
        self.client = client
        self.max_time = 0

        # test if user enabled reading notebook
        user, ts = self.write_file(TestFramework.STUDENT_FILE)
        client.user = user
        self.max_time = ts

    def write_file(self, fn=STUDENT_FILE):

        # download the notebook (it's a json file) if it's readable
        text = install_gd_file(self.notebook_id, TestFramework.JSON_FILE, force=True, persist=True)
        if text is None or not text.find('{"nbformat') == 0:
            raise Exception("Make notebook viewable")

        py_code, user, ts = self.parse(text)
        #{"timestamp": 1583470815612}

        # if you encounter a "year is out of range" error the timestamp
        # may be in milliseconds, try `ts /= 1000` in that case
        tsf = ts/1000.0
        logger.log("using ", ts, datetime.fromtimestamp(tsf).strftime('%Y-%m-%d %H:%M:%S'))
        #logger.log(time.strftime("%D %H:%M", time.localtime(tsf)))
        with open(fn, 'w') as fd:
            fd.write(py_code)

        return user, ts

    def parse(self, text):

        '''
           "metadata":{"id":"2q1l6oLFOjxV","colab_type":"code","outputId":"8a9a82ab-e6c8-4a86-a0ac-d6a045a519da","executionInfo":{"status":"ok","timestamp":1583528004120,"user_tz":480,"elapsed":624,
           "user":{"displayName":"mike haberman

           "metadata":{
           "colab":{"name":"Copy of Chapter 10 - Learning without Supervision.ipynb",
               "provenance":[
                  {"file_id":"https://github.com/fbkarsdorp/python-course/blob/master/answerbook/Chapter%2010%20-%20Learning%20without%20Supervision.ipynb",
                   "timestamp":1583470815612}]},
        '''

        code = json.loads(text)

        # creation timestamp
        metadata = code['metadata']
        colab = metadata.get('colab', {})
        items = colab.get('provenance', [])
        timestamp = 0
        if len(items) > 0:
            timestamp = items[0].get('timestamp', 0)

        lines = []
        user = None
        max_time = timestamp
        for cell in code['cells']:
            if cell['cell_type'] == 'code':
                meta = cell.get('metadata', {})
                info = meta.get('executionInfo', {})
                ts = int(info.get('timestamp', 0))
                if ts > max_time:
                    max_time = ts
                user_info = info.get('user', None)
                if user is not None and user_info is not None:
                    user = {'name': user['displayName'], 'id': user['userId']}

                for line in cell['source']:
                    if len(line) > 0 and line[0] not in ['!', '%']:
                        clean = line.rstrip()
                        lines.append(clean)
            elif cell['cell_type'] == 'markdown':
                pass
                #print('# -------- markdown --------')
                #for line in cell['source']:
                #    print("#", line, end='')
                #print('\n')

        return '\n'.join(lines), user, max_time

    #
    # PUBLIC API
    #

    def hello_world(self):
        tf = self.max_time/1000
        tf = time.ctime(tf)
        if self.client.backend:
            print("Hello! (backend)", self.max_time, tf)
        else:
            print("Hello!", tf)

    def test_function(self, fn):

        assert fn is not None, "fn is None"

        if callable(fn):
            fn = fn.__name__

        u, ts = self.write_file(TestFramework.STUDENT_FILE)
        score, max_score = self.client.test_function(TestFramework.STUDENT_FILE, fn)
        print(score, max_score)

    def test_with_button(self, fn):

        if self.client.backend:
            return 'unable to test locally'

        if callable(fn):
            fn = fn.__name__

        try:
            import ipywidgets as widgets
            from IPython.display import display, clear_output

            button = widgets.Button(description="Test " + fn)
            output = widgets.Output()

            def on_button_clicked(input):
                clear_output()
                u, ts = self.write_file(TestFramework.STUDENT_FILE)
                # send code off to be tested !
                score, max_score = self.client.test_function(TestFramework.STUDENT_FILE, fn)

                # Display the message within the output widget.
                with output:
                    #print("Button clicked.", fn, input)
                    if score == max_score:
                        button.style = widgets.ButtonStyle(button_color='green')
                        button.description = 'PASS'
                        print("score ", score)
                    else:
                        button.style = widgets.ButtonStyle(button_color='red')
                        button.description = 'FAIL: {}/{}'.format(score, max_score)
                        print("if you change", fn, "save the notebook before retesting")
                    #button.disabled = True

            button.on_click(on_button_clicked)
            display(button, output)

        except ImportError as e:
            return 'unable to test: ' + str(e)


#
# assumes this file Tools.py is already installed via install_file
#

'''
in a notebook to install a single file that's on a google drive:
TOOL_ID = '1JaBOzRUM3pgbYVFpU640SjxCjH7SH98N'   # keep this: google id of Tools.py
install_file(TOOL_ID, 'Tool.py', True)
'''




