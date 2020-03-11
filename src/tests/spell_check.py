

import sys
sys.path.append('..')

from utils import Parser
from utils import Tools

n_id ='1ymVhzIS-TCKhOx28jWEQ3E2IxWscGwwA'
sys.path.append('..')
#txt = Tools.install_gd_file(n_id, 'tmp.txt', force=True)
txt = Tools.install_gd_file(n_id, 'tmp.txt', force=True, persist=True)

parser = Parser.NBParser()
txt = parser.parse_markdown(txt)
open('what.txt', 'w').write(txt)

def clean_markdown(txt):
    clean = []
    for l in txt.split('\n'):
        line = l.strip()
        if len(line) == 0:
            continue
        if line.startswith('$') and line.endswith('$'):
            continue
        tokens = []
        for token in line.split():
            token = token.replace('$', ' ')
            token = token.replace('[', ' ')
            token = token.replace(']', ' ')
            token = token.replace('\\', ' ')
            token = token.replace('#', '')
            token = token.replace('*', '')
            tokens.append(token)
        clean.append(' '.join(tokens) + '\n')
    return '\n'.join(clean)

print(clean_markdown(txt))

