
# This module allows for testing colab code
#
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

def hello_world():
    print("Hello!")


class TestFramework(object):

    def __init__(self, notebook_id, lesson_id):
        self.notebook_id = notebook_id
        self.lesson_id   = lesson_id
        self.user = None

        # make sure notebook is readable
        txt = install_gd_file(notebook_id, 'file.json', force=True, persist=False)
        if not txt.find('{"nbformat') == 0:
            raise Exception("Make notebook viewable")

    def convert(self):
        text = install_gd_file(self.notebook_id, 'file.json', force=True, persist=False)
        py_code = self.parse(text)
        with open('student.py', 'w') as fd:
            fd.write(py_code)

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

    def test_with_button(self, fn):
        import ipywidgets as widgets
        from IPython.display import display

        cells = self.parse(txt)

        name = fn.__name__
        button = widgets.Button(description="Test " + name)
        output = widgets.Output()

        def on_button_clicked(b):
            # Display the message within the output widget.
            with output:
                print(cells)
                print("Button clicked.", name)

        button.on_click(on_button_clicked)
        display(button, output)



#
# assumes this file Tools.py is already installed via install_file
#



if __name__ == '__main__':

    NOTEBOOK_ID = '1ymVhzIS-TCKhOx28jWEQ3E2IxWscGwwA'  # change me!!
    LESSON_ID = 'LinearAlgebra:1:1'  # keep this

    tester = TestFramework(NOTEBOOK_ID, LESSON_ID)

    txt = open('test.json').read()
    py_code = tester.parse(txt)
    with open('wow.py', 'w') as fd:
        fd.write(py_code)

    '''
    in a notebook to install a single file that's on a google drive:
    TOOL_ID = '1JaBOzRUM3pgbYVFpU640SjxCjH7SH98N'   # keep this: google id of Tools.py
    install_file(TOOL_ID, 'Tool.py', True)
    '''
