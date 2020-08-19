import os


def mkdir(path):
    try:
        os.stat(path)
    except:
        os.mkdir(path)


def path_exists(path):
    try:
        os.stat(path)
        return True
    except:
        return False
