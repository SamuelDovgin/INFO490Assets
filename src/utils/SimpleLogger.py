
class SimpleLogger(object):

    __instance = None

    def __new__(cls):
        if SimpleLogger.__instance is None:
            SimpleLogger.__instance = object.__new__(cls)
        SimpleLogger.__instance
        return SimpleLogger.__instance

    def __init__(self):
        self.logger = open("debug_log.txt", "w")

    def log(self, *args):
        to_write = " ".join([str(a) for a in args])
        self.logger.write(to_write + '\n')
        self.logger.flush()


logger = SimpleLogger()
