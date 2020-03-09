

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

    def test_grader_fn():
        tuple = tester.test_function('simple_addr')
        print(tuple)

    def test_grader():
        tuple = tester.test_notebook()
        # use leaderboard field to fill in data to be plotted
        print(tuple)

    def debug_test():
        # use the client directly
        zip_file = Client.create_zipfile('solution.py')
        response = Client.send_zip(Client.SERVER, zip_file, LESSON_ID, 'simple_add')
        error   = response['error_code']
        if error is None:
            payload = response['payload']
            print(payload['test_result'])
        else:
            print('ERROR', error)

    def test_parser(fn, outfn):
        txt = open(fn).read()
        py_code,user,ts = tester.parse(txt)
        print(user, ts)
        with open(outfn, 'w') as fd:
            fd.write(py_code)

    #debug_test()
    #test_parser('test.json', outfn='wow.py')

    #test_grader()
    test_grader_fn()

    #
    # note this downloads the file (solution.py and solution.json)
    # when you do python solution.py
    # it needs to fail on the import ... otherwise
    # it's possible that the test inside solution.py will overwrite itself
    # when it downloads the same file on top of itself
    # but it should still run fine
    #
