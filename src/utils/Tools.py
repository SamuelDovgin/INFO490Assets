
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
from utils import Client, Parser




'''
#
# it's important that this fails on the test/server side
# so Nop is used when the solution.py is run directly
#
def install_testing_framework(lesson_id, notebook_id):
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
        return Tools.TestFramework(lesson_id, notebook_id)
    except ImportError as e:
        # happens on the test side, or if code never mounted
        return Nop(str(e))

tester = install_testing_framework(LESSON_ID, NOTEBOOK_ID)
tester.hello_world()
'''

def install_gd_file(doc_id, force=True, filename=None):

    import os
    if not force and os.path.exists(filename):
        logger.log("reading cached version")
        with open(filename, 'r') as fd:
           return fd.read()

    #
    # possible 403 if attempt is made too many times to download?
    # seems to be temporary -- don't fire off too many requests
    #
    baseurl = "https://docs.google.com/uc"
    baseurl = "https://drive.google.com/uc"
    #
    # can help by switching the baseurl
    #

    params = {"export": "download", "id": doc_id}
    url = baseurl + "?" + urllib.parse.urlencode(params)

    try:

        def v1():
            logger.log('fetching google doc', url)
            r = urllib.request.urlopen(url)
            status = r.getcode()
            if status != 200:
                print("unable to download notebook")
                print('status', r.status_code)
                return None
            return str(r.read().decode('UTF-8'))

        def v2():
            #r = requests.get(baseurl, params)
            logger.log('fetching google doc', url)
            r = requests.get(url)
            if r.status_code != 200:
                print(r.headers)
                print("unable to download notebook")
                print('status', r.status_code)
                return None
            return r.text

        text = v2()
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

    def __init__(self, lesson_id, notebook_id, client=None):

        if client is None:
            client = Client.ClientTest(lesson_id, notebook_id)

        # both need to be done before write_file
        self.client = client
        self.parser = Parser.NBParser()

        # test if user enabled world reading notebook
        self.write_file(TestFramework.STUDENT_FILE)

    def last_exec(self):
        import time
        now = (time.time() * 1000)
        max_time = self.parser.get_last_exectime(TestFramework.JSON_FILE)
        print( (now - max_time)/1000 )

    def write_file(self, fn=STUDENT_FILE, as_is=False, remove_magic_cells=True):

        # download the notebook (it's a json file) if it's readable
        nb_id = self.client.get_meta().notebook_id

        text = install_gd_file(nb_id, force=True, filename=TestFramework.JSON_FILE)
        if text is None or not text.find('{"nbformat') == 0:
            raise Exception("Make notebook viewable")

        py_code, min_ts, max_ts, user = self.parser.parse_code(text, as_is=as_is, remove_magic_cells=remove_magic_cells)
        with open(fn, 'w') as fd:
            fd.write(py_code)

        # {"timestamp": 1583470815612}
        # if you encounter a "year is out of range" error the timestamp
        # may be in milliseconds, try `ts /= 1000` in that case
        tsf = max_ts/1000.0
        logger.log("using ", max_ts, datetime.fromtimestamp(tsf).strftime('%Y-%m-%d %H:%M:%S'))
        # logger.log(time.strftime("%D %H:%M", time.localtime(tsf)))

        self.client.get_meta().update(min_ts, max_ts, user)

    #
    # PUBLIC API
    #

    def hello_world(self):
        min_ts = self.client.get_meta().min_time
        max_ts = self.client.get_meta().max_time
        tf = min_ts/1000
        min_tf = time.ctime(tf)
        tf = max_ts/1000
        max_tf = time.ctime(tf)
        diff = int((max_ts - min_ts)/1000)

        if self.client.is_backend:
            print("Hello! (backend)")
        else:
            print("Hello!")
        print("{:s}\n{:s} ({:d})".format(min_tf, max_tf, diff))

    def is_notebook_valid_python(self):
        self.write_file(TestFramework.STUDENT_FILE, as_is=True)
        e, r = self.client.test_file(TestFramework.STUDENT_FILE)
        return e is None, e

    def clean_notebook_for_download(self):
        self.write_file(TestFramework.STUDENT_FILE, as_is=False, remove_magic_cells=True)
        e, r = self.client.test_file(TestFramework.STUDENT_FILE)
        return e is None, e

    def test_notebook(self):
        self.write_file(TestFramework.STUDENT_FILE, as_is=False, remove_magic_cells=True)
        e, r = self.client.test_file(TestFramework.STUDENT_FILE)
        #
        # TODO: make result user friendly for display
        #
        return e, r

    def test_function(self, fn):

        assert fn is not None, "fn is None"

        if callable(fn):
            fn = fn.__name__

        self.write_file(TestFramework.STUDENT_FILE, as_is=False, remove_magic_cells=True)
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
