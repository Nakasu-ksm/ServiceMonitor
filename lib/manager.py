def _init(data):
    global manager
    manager = data


def set_error(index):
    manager[index]["status"] = 1


def set_success(index):
    manager[index]["status"] = 0
