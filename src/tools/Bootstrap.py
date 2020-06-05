import os
import sys

'''
OLD
def install_info490_repo():
  import os
  import sys
  INSTALL_PATH = '/content/info490' # keep as is
  if not os.path.exists(INSTALL_PATH):
    os.mkdir(INSTALL_PATH)
  #!git clone https://github.com/NSF-EC/INFO490Assets.git info490/INFO490Assets
  #!git clone https://github.com/habermanUIUC/DMAPTester.git info490/DMAPTester
  #if you need to do a pull (rare, unless instructed to) uncomment the following
  #!cd info490/INFO490Assets; git pull; cd .. 
  #!cd info490/DMAPTester; git pull; cd ..

  ASSET_PATH = "{:s}/{:s}".format(INSTALL_PATH, "INFO490Assets/src")
  if ASSET_PATH not in sys.path:
    sys.path.append(ASSET_PATH)

  from tools import IDE
  import importlib
  importlib.reload(IDE)
  return IDE.ColabIDE(LESSON_ID, NOTEBOOK_ID, reload=True)

ide = install_info490_repo()
tester = ide.tester
reader = ide.reader
'''

''' 
COLAB INSTALL

def install_info490_repo(reload=False):
  try:
    import os, sys
    INSTALL_PATH = '/content/info490' # keep as is
    if not os.path.exists(INSTALL_PATH):
      os.mkdir(INSTALL_PATH)
    !git clone https://github.com/NSF-EC/INFO490Assets.git info490/INFO490Assets
    !git clone https://github.com/habermanUIUC/DMAPTester.git info490/DMAPTester
    if reload:
      !cd info490/INFO490Assets; git pull; cd .. 
      !cd info490/DMAPTester; git pull; cd .. 

    ASSET_PATH = "{:s}/{:s}".format(INSTALL_PATH, "INFO490Assets/src")
    if ASSET_PATH not in sys.path:
      sys.path.append(ASSET_PATH)
    from tools import IDE
    if reload:
      import importlib
      importlib.reload(IDE)
    return IDE.ColabIDE(LESSON_ID, NOTEBOOK_ID, reload=reload)
  except Exception as e:
    class Nop(object):
        def __init__(self, e): self.e = e
        def nop(self, *args, **kw): return("unable to test:" + self.e, None)
        def __getattr__(self, _): return self.nop 
    class IDE():
      tester=Nop(str(e))
      reader=Nop(str(e))
    return IDE()

ide = install_info490_repo(True)
'''

INSTALL_DIR = 'info490'
ASSET_REPO = "https://github.com/NSF-EC/INFO490Assets.git"
TEST_REPO  = "https://github.com/habermanUIUC/DMAPTester.git"
ASSET_DST = "INFO490Assets"
TEST_DST = "DMAPTester"


class BootStrap(object):

    def __init__(self,):

        # won't work if BootStrap is softlinked
        #fq = os.path.abspath(os.path.dirname(__file__))
        #install_path = os.path.dirname(fq)

        install_path = os.getcwd()
        print(install_path)

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
            cmd = "cd {:s} ; git pull".format(asset_dir)
            os.system(cmd)
            cmd = "cd {:s} ; git pull".format(test_dir)
            os.system(cmd)

        SRC_PATH = "{:s}/{:s}".format(asset_dir, "src")
        if SRC_PATH not in sys.path:
            sys.path.append(SRC_PATH)


if __name__ == '__main__':
    boot = BootStrap()
    from tools import IDE
    print('YES')


