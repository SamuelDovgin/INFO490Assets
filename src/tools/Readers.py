import os
import sys

'''
from dmap.lessons.tfidf.lib import Util
text = Util.read_local_file('./info490/assets/src/dmap/lessons/tfidf/data/cith.txt')
OR
use the reader !!!
'''

GIT_ROOT = 'https://raw.githubusercontent.com/NSF-EC/INFO490Assets/master/src'

def in_path(dir):
    for p in sys.path:
        if p.find("/src") >= 0:
            return True
    return False


class AssetReader(object):

    def __init__(self, lesson_id, debug=False):

        self.debug = debug
        parts = lesson_id.lower().split(':')
        if len(parts) == 2:
            classroom = parts[0]  # DMAP
            tag = parts[1]        # tfidf
        else:
            classroom = parts[0]   # dmap
            dir_ignore = parts[1]  # data
            tag = parts[2]         # color

        # e.g. /dmap/lessons/
        base_path = "{:s}/lessons".format(classroom)

        self.url = "{git:s}/{base:s}/{tag:s}".format(git=GIT_ROOT,base=base_path, tag=tag)
        if debug:
            print('URL Assets', self.url)

        # root for remote fetching
        # set on install: /content/info490/assets
        fq = os.path.abspath(os.path.dirname(__file__))
        asset_dir = os.path.dirname(fq)
        assert asset_dir.find('/src') > 0, "bad asset path " + asset_dir
        if asset_dir not in sys.path:
            sys.path.append(asset_dir)

        base_dir = "{:s}/{:s}".format(asset_dir, base_path)
        self.lesson_base = "{:s}/{:s}".format(base_dir, tag)
        if debug:
            print('File Assets', self.lesson_base)

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

    def path_for_data(self, filename):
        return "{:s}/data/{:s}".format(self.lesson_base, filename)

    # better for clients to use LessonUtil.py
    def read_data_file(self, filename):
        fn = "{:s}/data/{:s}".format(self.lesson_base, filename)
        with open(fn, 'r') as fd:
            return fd.read()

    def read_local(self, filename):
        fn = "{:s}/{:s}".format(self.lesson_base, filename)
        with open(fn, 'r') as fd:
            return fd.read()

    def view_section(self, section, remote=False):
        section = int(section)
        if remote:
            url = "{:s}/html/section{section:02d}.html".format(self.url, section=section)
            try:
                import requests
                r = requests.get(url)
                r.encoding = 'utf-8'
                if r.status_code == requests.codes.ok:
                    text = r.text
                else:
                    text = "Error on fetch:" + str(r.status_code)
                    text += "\n" + url
                    print(text)
            except Exception as e:
                text = "Unable to get" + url
                text += "\n"+str(e)
                print(text)
        else:
            try:
                fq_path = "html/section{:02d}.html".format(section)
                text = self.read_local(fq_path)
            except FileNotFoundError:
                text = "File Not Found: " + fq_path
                print(text)

        if self.player:
            import IPython
            from IPython.display import display, clear_output
            #print('nb', len(text))
            display(IPython.display.HTML(text))
        else:
            #print('txt', len(text))
            print(text)

        # avoid printing anything out
        # way to suppress output on the return ??
        return None


if __name__ == "__main__":

   print('yes')
   tag = 'DMAP:dictorder'
   reader = AssetReader(tag)
   #print(reader.view_section(1, remote=True))
   #print(reader.view_section(1, remote=False))
