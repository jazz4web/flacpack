import importlib.util

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


def parse_field(pattern, filename, content):
    for i in range(len(content)):
        box = pattern.match(content[i])
        if box:
            break
    content[i] = f'FILE "{filename}" WAVE'
