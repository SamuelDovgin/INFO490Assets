
import json


class ParseValues(object):
    def __init__(self, code, user, timestamp):
        self.code = code
        self.user = user
        self.timestamp = timestamp


class NBParser(object):

    def __init__(self):
        pass

    def parse(self, text, remove_magic_cells=True, markdown=False):
        code = json.loads(text)

        # creation timestamp
        metadata = code['metadata']
        colab = metadata.get('colab', {})
        items = colab.get('provenance', [])
        timestamp = 0
        if len(items) > 0:
            timestamp = items[0].get('timestamp', 0)

        text = []
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
                    first_char = line.lstrip()
                    if first_char in ['!', '%']:
                        if remove_magic_cells:
                            # abandon ship on the entire cell
                            cell_code = []
                            break
                        else:
                            line = 'pass #' + line

                    if len(line) > 0:
                        clean = line.rstrip()
                        cell_code.append(clean)

                lines.extend(cell_code)

            elif markdown and cell['cell_type'] == 'markdown':
                for l in cell['source']:
                    text.append(l.strip())

        # return ParseValues('\n'.join(lines), user, max_time)
        if markdown:
            return "\n".join(text)

        return '\n'.join(lines), user, max_time
