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


def bytes_to_kb(b):
    return b/1000


def kb_to_mb(kilobytes):
    return kilobytes/1000


def mb_to_gb(megabytes):
    return megabytes/1000


def format_size(num):
    if num < 1000:
        # bytes
        return f'{num} B'
    # bytes
    if num >= 1000 and num < 1000000:
        # kilobytes
        return f'{round(bytes_to_kb(num), 1)} KB'
    elif num >= 1000000 and num < 1000000000:
        # megabytes
        return f'{round(kb_to_mb(bytes_to_kb(num)), 1)} MB'
    else:
        # gigabytes
        return f'{round(mb_to_gb(kb_to_mb(bytes_to_kb(num))), 1)} GB'
