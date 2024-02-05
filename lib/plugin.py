import importlib
import glob
from lib.check import *
def path_to_module_name(path):
    path = path.split("/")
    return path[0]+"."+path[1]

class Plugin():
    def __init__(self):
        self.manager = []
        Manager._init()
        self.load_module()
    def load_module(self):
        for path in glob.glob("plugin/*"):
            module = importlib.import_module(path_to_module_name(path))
            self.manager.append(module)

