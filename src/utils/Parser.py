
import json

from utils.SimpleLogger import logger

class ParseValues(object):
    def __init__(self, code, user, timestamp):
        self.code = code
        self.user = user
        self.timestamp = timestamp

def illegal_code(line):

    bad_news = ['from google.colab', 'import google', 'import IPython', 'from IPython']

    clean = line.lstrip()
    if len(clean) > 0 and clean[0] in ['!', '%']:
        return True

    remove_me = False
    for b in bad_news:
        if clean.find(b) >= 0:
            remove_me = True
            break

    return remove_me

class NBParser(object):

    def __init__(self):
        pass


    def parse_code(self, text, as_is=False, remove_magic_cells=True):
        code = json.loads(text)

        if as_is is True and remove_magic_cells is True:
            logger.log("warning, is_is flag takes priority")

        # creation timestamp
        metadata = code['metadata']
        colab = metadata.get('colab', {})
        items = colab.get('provenance', [])
        timestamp = 0
        if len(items) > 0:
            timestamp = items[0].get('timestamp', 0)

        lines = []
        user = None
        max_time = timestamp
        for cell in code['cells']:

            cell_code = []
            if cell['cell_type'] == 'code':
                meta = cell.get('metadata', {})
                info = meta.get('executionInfo', {})
                ts = int(info.get('timestamp', 0))
                if ts > max_time:
                    max_time = ts
                user_info = info.get('user', None)
                if user is not None and user_info is not None:
                    user = {'name': user['displayName'], 'id': user['userId']}

                for line in cell['source']:
                    if not as_is:
                        if illegal_code(line):
                            if remove_magic_cells:
                                cell_code = []
                                break
                            else:
                                line = 'pass #' + line
                        else:
                            # we will use the original line as is
                            pass

                    if len(line) > 0:
                        cell_code.append(line.rstrip())

                # option:  if a cell is mixed with magic and python
                '''
                !ls -la
                %% HTML 
                def partial():
                   for r in words:
                      w = r.lower()
                '''

                # 1.  if the cell is all magic remove it
                # 1.  if the cell is all magic remove it
                lines.extend(cell_code)

        return '\n'.join(lines), user, max_time

    def parse_markdown(self, text):

        code = json.loads(text)

        text = []
        for cell in code['cells']:
            if cell['cell_type'] == 'markdown':
                for l in cell['source']:
                    line = l.strip()
                    if len(line) > 0:
                        text.append(line.strip())

        return "\n".join(text)
