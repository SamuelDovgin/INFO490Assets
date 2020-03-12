
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

from utils.SimpleLogger import logger
from utils.Parser import NBParser

'''
#
# it's important that this fails on the test/server side
# so Nop is used when the solution.py is run directly
#
def install_testing_framework(notebook_id, lesson_id):
    import sys
    sys.path.append('info490/src')
    class Nop(object):
        def __init__(self, e): self.e = e
        # NOTE this returns two Values
        def nop(self, *args, **kw): return("unable to test:" + self.e, None)
        def __getattr__(self, _): return self.nop
    try:
        from utils import Tools,Client,Parser
        import importlib
        importlib.reload(Parser)
        importlib.reload(Tools)
        importlib.reload(Client)
        return Tools.TestFramework(notebook_id, Client.ClientTest(lesson_id))
    except ImportError as e:
        # happens on the test side, or if code never mounted
        return Nop(str(e))

tester = install_testing_framework(NOTEBOOK_ID, LESSON_ID)
tester.hello_world()
'''

def install_gd_file(doc_id, force=True, filename=None):

    import os
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
        if filename is not None:
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
        self.parser = NBParser()

        # test if user enabled reading notebook
        user, ts = self.write_file(TestFramework.STUDENT_FILE)
        client.user = user
        self.max_time = ts

    def write_file(self, fn=STUDENT_FILE, as_is=False, remove_magic_cells=True):

        # download the notebook (it's a json file) if it's readable
        text = install_gd_file(self.notebook_id, force=True, filename=TestFramework.JSON_FILE)
        if text is None or not text.find('{"nbformat') == 0:
            raise Exception("Make notebook viewable")

        py_code, user, ts = self.parser.parse_code(text, as_is=as_is, remove_magic_cells=remove_magic_cells)
        # {"timestamp": 1583470815612}

        # if you encounter a "year is out of range" error the timestamp
        # may be in milliseconds, try `ts /= 1000` in that case
        tsf = ts/1000.0
        logger.log("using ", ts, datetime.fromtimestamp(tsf).strftime('%Y-%m-%d %H:%M:%S'))
        # logger.log(time.strftime("%D %H:%M", time.localtime(tsf)))
        with open(fn, 'w') as fd:
            fd.write(py_code)

        return user, ts

    #
    # PUBLIC API
    #

    def hello_world(self):
        tf = self.max_time/1000
        tf = time.ctime(tf)
        if self.client.is_backend:
            print("Hello! (backend)", self.max_time, tf)
        else:
            print("Hello!", self.max_time, tf)

    def is_notebook_valid_python(self):
        u, ts = self.write_file(TestFramework.STUDENT_FILE, as_is=True)
        e, r = self.client.test_file(TestFramework.STUDENT_FILE)
        return e is None, e

    def clean_notebook_for_download(self):
        u, ts = self.write_file(TestFramework.STUDENT_FILE, as_is=False, remove_magic_cells=True)
        e, r = self.client.test_file(TestFramework.STUDENT_FILE)
        return e is None, e

    def test_notebook(self):
        u, ts = self.write_file(TestFramework.STUDENT_FILE, as_is=False, remove_magic_cells=True)
        e, r = self.client.test_file(TestFramework.STUDENT_FILE)
        #
        # TODO: make result user friendly for display
        #
        return e, r

    def test_function(self, fn):

        assert fn is not None, "fn is None"

        if callable(fn):
            fn = fn.__name__

        u, ts = self.write_file(TestFramework.STUDENT_FILE, as_is=False, remove_magic_cells=True)
        error, msg = self.client.test_function(TestFramework.STUDENT_FILE, fn)
        #score, max_score, msg = msg.split(':', maxsplit=2)
        return error, msg

    def test_with_button(self, fn):

        if self.client.is_backend:
            return 'unable to test with gui on server side'

        if callable(fn):
            fn = fn.__name__

        try:
            import ipywidgets as widgets
            from IPython.display import display, clear_output

            button = widgets.Button(description="Test " + fn)
            output = widgets.Output()

            def on_button_clicked(input):
                error, msg = self.test_function(fn)
                score, max_score, msg = msg.split(':', maxsplit=2)

                score = int(score)
                max_score = int(max_score)

                # print("Button clicked.", fn, input)
                # Display the message within the output widget.
                with output:

                    clear_output()  # also removes the button if put before output
                    print_warning = True
                    if error is None:
                        if msg.find('no tests') >= 0:
                            button.style = widgets.ButtonStyle(button_color='yellow')
                            button.description = 'No Tests'
                        elif score > 0 and score == max_score:
                            button.style = widgets.ButtonStyle(button_color='green')
                            button.description = 'Pass!'
                            print_warning = False
                        elif score > 0:
                            button.style = widgets.ButtonStyle(button_color='yellow')
                            button.description = 'More Work'
                        else:
                            button.style = widgets.ButtonStyle(button_color='red')
                            button.description = 'Fail'
                    else:
                        button.style = widgets.ButtonStyle(button_color='red')
                        button.description = 'FAIL: {}'.format(fn)
                        print(error)
                        msg = ''

                    if print_warning:
                        print(msg)
                        print("Using notebook version:", self.max_time)
                        print("If you change", fn, "save the notebook before retesting")

                    # since the button text changes
                    # disabling the button, makes sense
                    # otherwise, it's not clear that the user COULD press it again
                    # this way it forces the user to reload the cell
                    button.disabled = True

            button.on_click(on_button_clicked)
            display(button, output)

        except ImportError as e:
            return 'unable to test with gui: ', str(e)


#
# assumes this file Tools.py is already installed via install_file
#

'''
in a notebook to install a single file that's on a google drive:
TOOL_ID = '1JaBOzRUM3pgbYVFpU640SjxCjH7SH98N'   # keep this: google id of Tools.py
install_file(TOOL_ID, 'Tool.py', True)
'''
