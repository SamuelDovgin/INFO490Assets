
'''
Local Install Notes:
soft link to the DMAPTesting Framework
'''

''' 
COLAB INSTALL
def install_info490_repo():
  import os
  import sys
  INSTALL_PATH = '/content/info490' # keep as is
  if not os.path.exists(INSTALL_PATH):
    os.mkdir(INSTALL_PATH)
  !git clone https://github.com/NSF-EC/INFO490Assets.git info490/INFO490Assets
  !git clone https://github.com/habermanUIUC/DMAPTester.git info490/DMAPTester
  #if you need to do a pull (rare, unless instructed to) uncomment the following
  #!cd info490/INFO490Assets; git pull; cd .. 
  #!cd info490/DMAPTester; git pull; cd ..
  
  ASSET_PATH = "{:s}/{:s}".format(INSTALL_PATH, "INFO490Assets/src")
  if ASSET_PATH not in sys.path:
    sys.path.append(ASSET_PATH)
  from tools import IDE
  return IDE.ColabIDE(LESSON_ID, NOTEBOOK_ID)

ide = install_info490_repo()
tester = ide.tester
reader = ide.reader
tester.hello_world()
'''

import os
import sys


class Nop(object):

    def __init__(self, e):
        self.e = e

    def nop(self, *args, **kw):
        return "unable to test:" + self.e, None

    def __getattr__(self, _):
        return self.nop


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


class ColabIDE(object):

    def __init__(self, lesson_id, notebook_id, root='/content/info490', reload=False):
        if root is None:
            # grab from env
            root = os.environ.get('ROOT_PATH', None)

        asset_path = "{:s}/{:s}".format(root, '/INFO490Assets/src')
        test_path = "{:s}/{:s}".format(root, '/DMAPTester/src')
        assert os.path.isdir(asset_path), "no assets found" + asset_path
        assert os.path.isdir(test_path), "no tests found" + test_path

        if asset_path not in sys.path:
            sys.path.append(asset_path)
        if test_path not in sys.path:
            sys.path.append(test_path)

        self.root = root
        self.asset_path = asset_path
        self.test_path = test_path

        self.tester, self.reader = install_colab_framework(lesson_id, notebook_id, reload)



