
import json


class ParseValues(object):
    def __init__(self, code, user, timestamp):
        self.code = code
        self.user = user
        self.timestamp = timestamp


class NBParser(object):

    def __init__(self):
        pass


    def parse_code(self, text, as_is=False, remove_magic_cells=True):
        code = json.loads(text)

        if as_is is True and remove_magic_cells is True:
            print("warning, is_is flag takes priority")

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
                        clean = line.lstrip()
                        t1 = clean.find('import IPython') >= 0 or clean.find('from IPython') >= 0
                        t2 = len(clean) > 0 and clean[0] in ['!', '%']
                        if t1 or t2:
                            if remove_magic_cells:
                                cell_code = []
                                break
                            else:
                                line = 'pass #' + line

                    if len(line) > 0:
                        clean = line.rstrip()
                        cell_code.append(clean)

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
