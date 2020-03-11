

'''
python 2.7 hack
import sys
import os
sys.path.append('..')
parent_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../utils')
print('PARENT', parent_dir, __file__)
sys.path.insert(0, parent_dir)
print(sys.path)
import Tools
import Client
'''


# need python 3.6+
import sys
sys.path.append('..')

from utils import Client
from utils import Tools, Parser

def css_styling(snip):
    from IPython.core.display import HTML
    import requests
    styles = requests.get('https://raw.githubusercontent.com/fbkarsdorp/python-course/master/styles/custom.css')
    txt = styles.text
    idx = txt.find('<style>')
    return HTML(txt[idx:] + snip)

#css_styling('<div class="1warning">TEST</div>'

if __name__ == '__main__':

    import json

    NOTEBOOK_ID = '1ymVhzIS-TCKhOx28jWEQ3E2IxWscGwwA'  # change me!!
    NOTEBOOK_ID = '1GDCmobYye_kk28N35oK8i_BZdSSTyFsT'
    LESSON_ID = 'LinearAlgebra:1:1'  # keep this
    LESSON_ID = '00'  # keep this

    # needs to be local server NOT THE WAN address
    #SERVER = 'http://192.168.1.78:8080/testzip'

    client = Client.ClientTest(LESSON_ID)

    def test_grader_fn():
        tester = Tools.TestFramework(NOTEBOOK_ID, client)
        tester.hello_world()
        tuple = tester.test_function('simple_add')
        print(tuple)

    def test_is_ready_to_submit():
        tester = Tools.TestFramework(NOTEBOOK_ID, client)
        tuple = tester.is_notebook_valid_python()
        print(tuple)

    def test_is_ready_to_download():
        tester = Tools.TestFramework(NOTEBOOK_ID, client)
        tuple = tester.clean_notebook_for_download()
        print(tuple)

    def test_grader():
        tester = Tools.TestFramework(NOTEBOOK_ID, client)
        tester.hello_world()
        tuple = tester.test_notebook()
        # use leaderboard field to fill in data to be plotted
        print(tuple)

    def debug_test(filename, fn):
        # use the client directly
        zip_file = Client.create_zipfile(filename)
        response = Client.send_zip(Client.SERVER, zip_file, LESSON_ID, fn)
        error   = response['error_code']
        if error is None:
            payload = response['payload']
            print(payload['test_result'])
        else:
            print('ERROR', error)

    def test_parser(fn, outfn):
        txt = open(fn).read()
        parser = Parser.NBParser()
        py_code,user,ts = parser.parse(txt)
        print(user, ts)
        with open(outfn, 'w') as fd:
            fd.write(py_code)

    # test a local file (MUST be named solution.py as the tests import this)
    #debug_test('solution.py', 'simple_add')
    #test_parser('test.json', outfn='wow.py')


    # these download notebook
    test_grader()
    #test_grader_fn()

    #test_is_ready_to_submit()
    #test_is_ready_to_download()


    #
    # note this downloads the file (solution.py and solution.json)
    # when you do python solution.py
    # it needs to fail on the import ... otherwise
    # it's possible that the test inside solution.py will overwrite itself
    # when it downloads the same file on top of itself
    # but it should still run fine
    #
    # TEST student asks to test simple_add, infinite loop
    # TEST student asks to test simple_add,  BUT there is no simple_add function in the code
    # TEST student asks to test simple_addr, BUT there is no test for that
    #
