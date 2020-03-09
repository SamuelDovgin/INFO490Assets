

import sys
sys.path.append('..')
from utils import Tools
from utils import Client

def css_styling(snip):
    from IPython.core.display import HTML
    import requests
    styles = requests.get('https://raw.githubusercontent.com/fbkarsdorp/python-course/master/styles/custom.css')
    txt = styles.text
    idx = txt.find('<style>')
    return HTML(txt[idx:] + snip)

#css_styling('<div class="warning">TEST</div>'

if __name__ == '__main__':

    import json

    NOTEBOOK_ID = '1ymVhzIS-TCKhOx28jWEQ3E2IxWscGwwA'  # change me!!
    LESSON_ID = 'LinearAlgebra:1:1'  # keep this
    LESSON_ID = '00'  # keep this

    # needs to be local server NOT THE WAN address
    #SERVER = 'http://192.168.1.78:8080/testzip'

    client = Client.ClientTest(LESSON_ID)
    tester = Tools.TestFramework(NOTEBOOK_ID, client)
    tester.hello_world()

    def test_grader():
        tuple = tester.test_function('simple_add')
        print(tuple)

    def v1():
        zip_file = Client.create_zipfile('solution.py')
        response = Client.send_zip(Tools.SERVER, zip_file, LESSON_ID, 'simple_add')

        error   = response['error_code']
        if error is None:
            payload = response['payload']
            print(payload['test_result'])
        else:
            print('ERROR', error)

    def test_parser():
        txt = open('test.json').read()
        py_code,user,ts = tester.parse(txt)
        print(user, ts)
        with open('wow.py', 'w') as fd:
            fd.write(py_code)

    test_grader()
