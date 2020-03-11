

import sys
sys.path.append('..')

from utils import Parser
from utils import Tools

import argparse
import re

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
            'scrollTo=Y6FQ_T8fB2nx)'
            p = r'scrollTo\s?=\s?[A-Za-z0-9_]+'
            token = re.sub(p, ' ', token)

            tokens.append(token)
        clean.append(' '.join(tokens) + '\n')
    return '\n'.join(clean)


tag_map = {
    '00': '1GDCmobYye_kk28N35oK8i_BZdSSTyFsT'
}
parser = argparse.ArgumentParser(description='Test python')
parser.add_argument('--tag', type=str, help='assignment tag', default='01', required=False)
args = parser.parse_args()

notebook_id = tag_map.get(args.tag, None)
if notebook_id is not None:
   txt = Tools.install_gd_file(notebook_id, force=True)
   parser = Parser.NBParser()
   txt = parser.parse_markdown(txt)
   clean = clean_markdown(txt)

'''
python spell_check.py -tag > spell.txt
cat spell.txt | aspell list --encoding utf-8
1. Do this first (so you can add words to the dictionaryl
aspell check out.txt

LIST of words
cat spell.txt | aspell list --encoding utf-8 | uniq

LIST words and options
cat spell.txt | aspell pipe --encoding utf-8 | uniq | grep -v \* | grep -v '^$'
'''
