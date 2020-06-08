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
    'base': '/dmap/lessons/',  # ending slash is important
    'DMAP:INTRO': {
        'base': 'intro',
    },
    'DMAP:dictorder': {
        'base': 'dictorder',
    },
    'DMAP:TFIDF': {
        'base': 'tfidf',
    },
}


def in_path(dir):
    for p in sys.path:
        if p.find("/src") >= 0:
            return True
    return False


class AssetReader(object):

    def __init__(self, lesson_id):

        parts = lesson_id.split(':', 2)
        classroom = parts[0] # DMAP
        tag = parts[1]  # tfidf
        url = '"http://raw.githubusercontent.com/NSF-EC/INFO490Assets/master/src/dmap/lessons/{:s}'.format(tag)
        url += '/html/section{section:d}.html"'
        self.url = url

        # set on install: /content/info490/assets
        fq = os.path.abspath(os.path.dirname(__file__))
        asset_dir = os.path.dirname(fq)
        assert asset_dir.find('/src') > 0, "bad asset path " + asset_dir
        if asset_dir not in sys.path:
            sys.path.append(asset_dir)

        base_dir = asset_dir + LESSON_MAP.get('base', None)
        assert base_dir is not None, "bad Reader config"

        if lesson_id in LESSON_MAP:
            lesson_base = LESSON_MAP[lesson_id].get('base', tag)
            self.lesson_base = base_dir + lesson_base
        else:
            self.lesson_base = base_dir + tag

        # allow imports of lib
        # these files MUST be available on test framework too
        lib_dir = "{:s}/lib".format(self.lesson_base)
        if lib_dir not in sys.path:
            sys.path.append(lib_dir)

        try:
            from IPython.display import display, clear_output
            self.player = display
        except ImportError:
            print("IPython not installed")
            self.player = None

    def read_data_file(self, filename):
        fn = "{:s}/data/{:s}".format(self.lesson_base, filename)
        with open(fn, 'r') as fd:
            return fd.read()

    def read_local(self, filename):
        fn = "{:s}/{:s}".format(self.lesson_base, filename)
        with open(fn, 'r') as fd:
            return fd.read()

    def view_section(self, section, remote=False):

        if remote:
            try:
                import requests
                url = self.url.format(section=section)
                text = requests.get(url).text
            except Exception as e:
                text = "Unable to get" + url
                text += "\n"+str(e)
        else:
            try:
                page = str(section)
                fq_path = "html/section{:s}.html".format(page)
                text = self.read_local(fq_path)
            except FileNotFoundError:
                text = "File Not Found: " + fq_path

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