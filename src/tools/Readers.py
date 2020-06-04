import os
import sys


'''
from dmap.lessons.tfidf.lib import Util
text = Util.read_local_file('./info490/assets/src/dmap/lessons/tfidf/data/cith.txt')

OR
use the reader !!!

'''

#
# TODO:  put in config file, fetch it
#
LESSON_MAP = {
    'base': '/dmap/lessons/',
    'DMP:TFIDF': {
        'base': 'tfidf',
        'parts': 4,
    },
}


def in_path(dir):
    for p in sys.path:
        if p.find("/src") >= 0:
            return True
    return False


class AssetReader(object):

    def __init__(self, lesson_id):

        # set on install: /content/info490/assets
        fq = os.path.abspath(os.path.dirname(__file__))
        asset_dir = os.path.dirname(fq)
        assert asset_dir.find('/src') > 0, "bad asset path " + asset_dir
        if asset_dir not in sys.path:
            sys.path.append(asset_dir)

        base_dir = asset_dir + LESSON_MAP.get('base', '')
        if lesson_id in LESSON_MAP:
            lesson_base = LESSON_MAP[lesson_id].get('base', '')
            print(lesson_base)
            self.lesson_base = base_dir + lesson_base
        else:
            self.lesson_base = base_dir

        try:
            from IPython.display import display, clear_output
            self.player = display
        except ImportError:
            print("IPython not installed")
            self.player = None

    # 'data/cith.txt'
    def read_local(self, filename):
        fn = "{:s}/{:s}".format(self.lesson_base, filename)
        with open(fn, 'r') as fd:
            return fd.read()

    def view(self, page):

        page = str(page)
        fq_path = "part{:s}.html".format(page)
        text = self.read_local(fq_path)

        if self.player:
            import IPython
            from IPython.display import display, clear_output
            display(IPython.display.HTML(text))
        else:
            print(text)

        # avoid printing anything out
        # way to suppress output on the return ??
        return None


'''
https://colab.research.google.com/drive/1Np-Si3PLn32v48QreAVEDVPX1S4MH81u#offline=false&sandboxMode=tru


import IPython, requests
LESSON_URL = 'https://raw.githubusercontent.com/NSF-EC/INFO490Assets/master/src/dmap/lessons/tfidf'
res = requests.get('{:s}/part0.html'.format(LESSON_URL));
display(IPython.display.HTML(res.text))


lesson_map_URL = {
    'base': 'https://raw.githubusercontent.com/NSF-EC/INFO490Assets/master/src/dmap/lessons/',
    'DMP:TFIDF' : {
        'base': 'tfidf',
        'parts': 4,
    }
}
class HtmlReader(object):
    def __init__(self, lesson_id):
        self.base = lesson_map.get('base') + lesson_map[lesson_id].get('base', 'na')
        try:
            from IPython.display import display, clear_output
            self.player = display
        except ImportError:
            self.player = None

    def _fetch(self, url):
        return requests.get(url).text

    def view(self, page):
        url = "{:s}/part{:d}.html".format(self.base, page)
        if self.player:
            import IPython
            from IPython.display import display, clear_output
            text = self._fetch(url)
            display(IPython.display.HTML(text))
        else:
            print('viewer not available')
        return ''
'''