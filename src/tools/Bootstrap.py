import os
import sys

INSTALL_DIR = 'info490'
ASSET_REPO = "https://github.com/NSF-EC/INFO490Assets.git"
TEST_REPO  = "https://github.com/habermanUIUC/DMAPTester.git"
ASSET_DST = "INFO490Assets"
TEST_DST = "DMAPTester"

'''
HACK: fix the DMAPTester so it returns 
only 1 value for all functions
'''
class Nop_TWO(object):
    def __init__(self, e):
        self.e = e
    def nop(self, *args, **kw):
        return "unable to test:" + self.e, None
    def __getattr__(self, _):
        return self.nop

class Nop_ONE(object):
    def __init__(self, e):
        self.e = e
    def nop(self, *args, **kw):
        return "unable to test:" + self.e
    def __getattr__(self, _):
        return self.nop

# TODO:  add Bootstrap noOp class in each of the Tests ??

def install_colab_framework(lesson_id, notebook_id, reload=False):
    try:
        from tf.notebook import Tools, Parser
        from tf.utils import Client
        from tools import Readers
        from tools import Utils

        if reload:
            import importlib
            print("reloading")
            importlib.reload(Tools)
            importlib.reload(Parser)
            importlib.reload(Client)
            importlib.reload(Readers)

        # pre test
        #url = Utils.build_google_drive_url(notebook_id)
        #text = Utils.read_remote1(url)

        ide = Tools.TestFramework(lesson_id, notebook_id)
        reader = Readers.AssetReader(lesson_id)

        return ide, reader

    except ImportError as e:
        return Nop(str(e)), Nop(str(e))

class BootStrap(object):

    def __init__(self):

        # won't work if BootStrap is softlinked
        #fq = os.path.abspath(os.path.dirname(__file__))
        #install_path = os.path.dirname(fq)

        install_path = os.getcwd()
        print("files located in", install_path)

        if not os.path.exists(INSTALL_DIR):
            os.mkdir(INSTALL_DIR)

        install_path = "{:s}/{:s}".format(install_path, INSTALL_DIR)
        asset_dir = "{:s}/{:s}".format(install_path, ASSET_DST)
        test_dir = "{:s}/{:s}".format(install_path, TEST_DST)

        if not os.path.exists(asset_dir):
            print("cloning git repos")
            cmd = "git clone {:s} {:s}".format(ASSET_REPO, asset_dir)
            os.system(cmd)
            cmd = "git clone {:s} {:s}".format(TEST_REPO, test_dir)
            os.system(cmd)
        else:
            print("reloading git repos")
            cmd = "cd {:s}; git pull".format(asset_dir)
            os.system(cmd)
            cmd = "cd {:s}; git pull".format(test_dir)
            os.system(cmd)

        src_path = "{:s}/{:s}".format(asset_dir, "src")
        if src_path not in sys.path:
            sys.path.append(src_path)
        src_path = "{:s}/{:s}".format(test_dir, "src")
        if src_path not in sys.path:
            sys.path.append(src_path)

    def create_ide(self, lesson_id, nb_id, reload=False):
        a, b = install_colab_framework(lesson_id, nb_id, reload=reload)
        class IDE(object):
            def __init__(self, t, r):
                self.tester = t
                self.reader = r
        return IDE(a, b)

