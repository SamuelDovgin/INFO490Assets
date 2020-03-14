
import json
import requests


from utils.SimpleLogger import logger
import utils.ZipLib as ZipLib

try:
    VERSION='03.12.2020'
    backend = False
    SERVER = 'http://75.156.71.78:8080'    # good for non-local client to test server
    SERVER = 'http://18.219.123.225:8080'  # AWS
    import ipywidgets as widgets
    from IPython.display import display
except ImportError as e:
    backend = True
    SERVER = 'http://127.0.0.1:8080'
    SERVER = 'http://18.219.123.225:8080'  # AWS
    SERVER = 'http://192.168.1.78:8080'    # local


class MetaData(object):

    def __init__(self, lesson_id, notebook_id):

        self.lesson_id = lesson_id
        self.notebook_id = notebook_id

        self.u_id   = None
        self.u_name = None
        self.min_time = 0
        self.max_time = 0

    def update(self, min_time, max_time, user=None):

        if self.min_time == 0 or min_time < self.min_time:
            self.min_time = min_time

        if self.max_time == 0 or max_time > self.max_time:
            self.max_time = max_time

        if self.u_id is None:
            self.u_id   = user['id']
            self.u_name = user['name']

    def kv(self):

        result = {
            'lesson_id': self.lesson_id,
            'notebook_id': self.notebook_id,
            'min_time': self.min_time,
            'max_time': self.max_time,
        }

        if self.u_id is not None:
            result['u_id']   = self.u_id
            result['u_name'] = self.u_name
        return result


class ClientTest(object):

    def __init__(self, lesson_id, notebook_id=0, server=None):

        assert lesson_id is not None, "bad lesson id"
        assert notebook_id is not None, "bad notebook id"

        meta = MetaData(lesson_id, notebook_id)

        if server is None:
            server = SERVER

        self.server      = server
        self.is_backend  = backend
        self.meta = meta

        logger.log("client version:", VERSION)
        logger.log("running in notebook:", backend is False)
        logger.log("server:", server)
        logger.log("data:", meta.kv())

    def get_meta(self):
        return self.meta

    def register_install(self, mount_time):

        end_point = "{:s}/register".format(self.server)

        post_data = {"notebook_id": self.meta.notebook_id,
                     "lesson_id": self.meta.lesson_id,
                     "u_id": self.meta.u_id,
                     "mount_time": mount_time}

        response = requests.post(end_point, data=post_data)
        if response.status_code != 200:
            logger.log('install did not register', response.status_code)
        else:
            logger.log('register install at', mount_time)

    def send_zip(self, zipfile, fn_name=None):

        end_point = "{:s}/testzip".format(self.server)

        with open(zipfile, 'rb') as fd:
            data = {'error_code': None, 'payload': {}}
            post_data = {"fn": fn_name}

            # add in the meta data (notebook, assignment, etc)
            kv = self.meta.kv()
            for k in kv:
                v = kv[k]
                if isinstance(v, dict):
                    v = json.dumps(kv[k])
                post_data[k] = v

            print('posting', post_data)
            response = requests.post(end_point, data=post_data,
                                     files={"archive": (zipfile, fd)})

            if response.status_code == 200:
                data = response.json()  # json.loads(r.text)
            else:
                data['error_code'] = response.status_code

            return data
    #
    # all tests must return TWO values (so NoOp will always work)
    #
    def test_file(self, filename, fn_name=None):

        logger.log("test", filename, self.get_meta().lesson_id, fn_name)

        zip_file = ZipLib.create_zipfile(filename)
        response = self.send_zip(zip_file, fn_name)
        logger.log(response)

        error = response['error_code']
        if error is None:
            payload = response['payload']
            result  = payload['test_result']

            if result['score'] != 100:
                # this gives some info back
                logger.log(json.dumps(result))
            return None, result
        else:
            return error, None

    def test_function(self, filename, fn_name):
        error, result = self.test_file(filename, fn_name)
        if error is None:
            for t in result['tests']:
                if t['name'] == fn_name:
                    return None, "{}:{}:{}".format(t['score'], t['max_score'], t['output'].strip())
            return None, "0:0:no tests for " + fn_name
        else:
            return error, "0:0:NA"

