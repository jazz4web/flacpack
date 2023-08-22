import os

from .system import detect_f_type


def grep(data, s):
    for each in data:
        if s in each:
            return each


def get_num(s):
    r = ''
    for i in s:
        if i.isnumeric():
            r += i
    if r:
        return int(r)
    return 0


def check_format(filename, store):
    if not os.path.exists(filename):
        raise FileNotFoundError(f'`{filename}` does not exist')
    data = detect_f_type(filename)
    snum = get_num(
        grep(data.split(b'\n'), b'total samples').decode('utf-8'))
    sr = get_num(
        grep(data.split(b'\n'), b'sample_rate').decode('utf-8'))
    if not sr:
        raise ValueError('unsupported sample rate')
    store['duration'] = snum / sr
    store['flac'] = os.path.realpath(filename)
    cue = f'{os.path.splitext(filename)[0]}.cue'
    if os.path.exists(cue):
        store['cue'] = os.path.realpath(cue)
    else:
        store['cue'] = None
