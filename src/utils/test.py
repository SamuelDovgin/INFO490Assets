

import Tools

def css_styling(snip):
    from IPython.core.display import HTML
    import requests
    styles = requests.get('https://raw.githubusercontent.com/fbkarsdorp/python-course/master/styles/custom.css')
    txt = styles.text
    idx = txt.find('<style>')
    return HTML(txt[idx:] + snip)

#css_styling('<div class="warning">TEST</div>'

if __name__ == '__main__':

    NOTEBOOK_ID = '1ymVhzIS-TCKhOx28jWEQ3E2IxWscGwwA'  # change me!!
    LESSON_ID = 'LinearAlgebra:1:1'  # keep this
    import Client
    tester = Tools.TestFramework(NOTEBOOK_ID, LESSON_ID, Client)
    tester.hello_world()

    def test_parser():
        import student
        txt = open('test.json').read()
        py_code = tester.parse(txt)
        with open('wow.py', 'w') as fd:
            fd.write(py_code)
