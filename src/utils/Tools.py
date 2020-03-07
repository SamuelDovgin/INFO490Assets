
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
import Client

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
    STUDENT_FILE = 'student.py'
    SERVER       = 'http://75.156.71.78:8080/testzip'

    def __init__(self, notebook_id, lesson_id):

        assert notebook_id is not None, "bad init"
        assert lesson_id is not None, "bad init"

        self.notebook_id = notebook_id
        self.user = None

        try:
            # test if user enabled reading notebook
            self.write_file(TestFramework.STUDENT_FILE)

            import ipywidgets as widgets
            from IPython.display import display
            self.client = Client.ClientTest(TestFramework.SERVER, lesson_id, self.user)
        except ImportError:
            self.client = None

    def hello_world(self):
        if self.client is not None:
           print("Hello!")
        else:
           print("Hello! (backend)")

    def write_file(self, fn=STUDENT_FILE):
        text = install_gd_file(self.notebook_id, TestFramework.JSON_FILE, force=True, persist=False)
        if not text.find('{"nbformat') == 0:
            raise Exception("Make notebook viewable")

        py_code = self.parse(text)
        with open(fn, 'w') as fd:
            fd.write(py_code)
        return py_code

    def parse(self, text):

        '''
           "metadata":{"id":"2q1l6oLFOjxV","colab_type":"code","outputId":"8a9a82ab-e6c8-4a86-a0ac-d6a045a519da","executionInfo":{"status":"ok","timestamp":1583528004120,"user_tz":480,"elapsed":624,
           "user":{"displayName":"mike haberman
        '''

        code = json.loads(text)
        lines = []
        for cell in code['cells']:
            if cell['cell_type'] == 'code':
                meta = cell.get('metadata', {})
                info = meta.get('executionInfo', {})
                user = info.get('user', None)
                if user is not None and self.user is None:
                    self.user = {'name': user['displayName'], 'id': user['userId']}

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

        return '\n'.join(lines)

    def test_function(self, fn):
        pass

    def test_with_button(self, fn):

        if self.client is None:
            return 'unable to test'

        try:
            import ipywidgets as widgets
            from IPython.display import display

            name = fn.__name__
            button = widgets.Button(description="Test " + name)
            output = widgets.Output()

            def on_button_clicked(b):
                self.write_file(TestFramework.STUDENT_FILE)
                response = self.client.test_file(TestFramework.STUDENT_FILE)
                # send code off to be tested !

                # Display the message within the output widget.
                with output:
                    # print(cells)
                    print("Button clicked.", name)

            button.on_click(on_button_clicked)
            display(button, output)

        except ImportError:
            return 'unable to test'


#
# assumes this file Tools.py is already installed via install_file
#

'''
in a notebook to install a single file that's on a google drive:
TOOL_ID = '1JaBOzRUM3pgbYVFpU640SjxCjH7SH98N'   # keep this: google id of Tools.py
install_file(TOOL_ID, 'Tool.py', True)
'''




