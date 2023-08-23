import importlib.util
import os

from mutagen.flac import FLAC, MutagenError


def check_format(filename, store):
    if not os.path.exists(filename):
        raise FileNotFoundError(f'`{filename}` does not exist')
    if importlib.util.find_spec('mutagen') is None:
        raise OSError('python3 module `mutagen` is not installed')
    try:
        flac = FLAC(os.path.realpath(filename))
        store['flac'] = flac
        store['duration'] = flac.info.total_samples / flac.info.sample_rate
    except MutagenError:
        store['flac'] = None
    cue = f'{os.path.splitext(filename)[0]}.cue'
    if os.path.exists(cue):
        store['cue'] = os.path.realpath(cue)
    else:
        store['cue'] = None
        store['cuefile'] = os.path.realpath(cue)
