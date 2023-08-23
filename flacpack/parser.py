import importlib.util
import io
import re
import shlex

from subprocess import Popen, PIPE
from mutagen.flac import FLAC

from .system import detect_c_type


def read_file(store):
    detect_c_type(store['cue'])
    if importlib.util.find_spec('chardet') is None:
        raise OSError('python3 module `charder` is not installed')
    from chardet import detect
    try:
        with open(store['cue'], 'rb') as f:
            enc = detect(f.read())['encoding']
            f.seek(0)
            store['cuecont'] = [line.decode(enc).rstrip() for line in f]
    except(OSError, ValueError):
        raise RuntimeError('impossible to read cuesheet')


def get_value(exp, content, file=False, index=False):
    pattern = re.compile(exp)
    for i in range(len(content)):
        box = pattern.match(content[i])
        if box:
            if file:
                return i
            if index:
                return box.group(1)
            return box.group(1).strip('"')


def f_to_seconds(s):
    mm, ss, ff = re.split(r'[:.]', s)
    return int(mm) * 60 + int(ss) + int(ff) / 75


def extract_metadata(store, filename):
    i = get_value(r'FILE +(.+)', store['cuecont'], file=True)
    store['cuecont'][i] = f'FILE "{filename}" WAVE'
    store['performer'] = get_value(r'^PERFORMER +(.+)', store['cuecont'])
    store['album'] = get_value(r'^TITLE +(.+)', store['cuecont'])
    store['genre'] = get_value(r'^REM GENRE +(.+)', store['cuecont'])
    store['disc id'] = get_value(r'^REM DISCID +(.+)', store['cuecont'])
    store['date'] = get_value(r'^REM DATE +(.+)', store['cuecont'])
    store['comment'] = get_value(r'^REM COMMENT +(.+)', store['cuecont'])
    r = list(reversed(store['cuecont']))
    store['tracks'] = get_value(r'^ +TRACK +(\d+) +(.+)', r, index=True)
    store['last'] = get_value(
        r'^ +INDEX 01 +(\d{2}:\d{2}:\d{2})', r, index=True)
    if not store['last'] or not store['tracks']:
        raise ValueError('bad cuesheet')
    store['last'] = f_to_seconds(store['last'])
    if store['last'] >= store['duration']:
        print('warning: cuesheet smells fishy')


def export_metadata(store):
    store['flac'].delete()
    store['flac']['artist'] = store['performer']
    store['flac']['album'] = store['album']
    store['flac']['genre'] = store['genre']
    store['flac']['date'] = store['date']
    store['flac']['tracks'] = store['tracks']
    store['flac']['disc id'] = store['disc id']
    store['flac']['comment'] = store['comment']
    store['flac']['cuesheet'] = '\n'.join(store['cuecont'])
    store['flac'].save()
