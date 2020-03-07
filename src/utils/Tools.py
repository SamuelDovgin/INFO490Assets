
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

def install_gd_file(doc_id, filename, force=False, persist=True):
  import os
  import urllib
  import urllib.parse
  import urllib.request
  #import importlib

  if not force and os.path.exists(filename):
    with open(filename, 'r') as fd:
      return fd.read()

  baseurl = "https://drive.google.com/uc"
  params = {"export" : "download", "id": doc_id}

  url = baseurl + "?" + urllib.parse.urlencode(params)
  r = urllib.request.urlopen(url)
  text = str(r.read().decode('UTF-8'))
  if persist:
     with open(filename, 'w') as fd:
       fd.write(text)
  return text



class TestFramework(object):

    JSON_FILE    = 'file.json'
    STUDENT_FILE = 'solution.py'

    def __init__(self, notebook_id, client):

        assert notebook_id is not None, "bad init"

        self.notebook_id = notebook_id
        self.client = client

        # test if user enabled reading notebook
        user = self.write_file(TestFramework.STUDENT_FILE)
        client.user = user


    def hello_world(self):
        if self.client.backend:
            print("Hello! (backend)")
        else:
            print("Hello!")

    def write_file(self, fn=STUDENT_FILE):
        # download the notebook (it's a json file) if it's readable
        text = install_gd_file(self.notebook_id, TestFramework.JSON_FILE, force=True, persist=False)
        if not text.find('{"nbformat') == 0:
            raise Exception("Make notebook viewable")

        py_code, user = self.parse(text)
        with open(fn, 'w') as fd:
            fd.write(py_code)
        return user

    def parse(self, text):

        '''
           "metadata":{"id":"2q1l6oLFOjxV","colab_type":"code","outputId":"8a9a82ab-e6c8-4a86-a0ac-d6a045a519da","executionInfo":{"status":"ok","timestamp":1583528004120,"user_tz":480,"elapsed":624,
           "user":{"displayName":"mike haberman
        '''

        code = json.loads(text)
        lines = []
        user = None
        for cell in code['cells']:
            if cell['cell_type'] == 'code':
                meta = cell.get('metadata', {})
                info = meta.get('executionInfo', {})
                user_info = info.get('user', None)
                if user is not None and user_info is None:
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

        return '\n'.join(lines), user

    def test_function(self, fn):

        assert fn is not None, "fn is None"

        if callable(fn):
            fn = fn.__name__

        self.write_file(TestFramework.STUDENT_FILE)
        response = self.client.test_function(TestFramework.STUDENT_FILE, fn)
        print(response)

    def test_with_button(self, fn):

        if self.client.backend:
            return 'unable to test locally'

        if callable(fn):
            fn = fn.__name__

        try:
            import ipywidgets as widgets
            from IPython.display import display

            button = widgets.Button(description="Test " + fn)
            output = widgets.Output()

            def on_button_clicked(input):
                self.write_file(TestFramework.STUDENT_FILE)
                response = self.client.test_function(TestFramework.STUDENT_FILE, fn)
                # send code off to be tested !

                # Display the message within the output widget.
                with output:
                    # print(cells)
                    print("Button clicked.", fn, input, response)

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




