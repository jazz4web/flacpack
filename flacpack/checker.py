"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
name:        flacpack
description: a simple tool packing
             cuesheet inside a FLAC file
license:     GNU GPLv3
author:      Jazz
contacts:    webmaster@codej.ru
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import importlib.util
import os

from mutagen.flac import FLAC, MutagenError
from .system import detect_c_type


def check_pic(args, store):
    dname = os.path.dirname(os.path.realpath(args.filename))
    pname = os.path.join(dname, args.pic)
    store['cfpic'] = None
    if os.path.exists(pname):
        detect_c_type(pname, text=False)
        store['cfpic'] = pname


def check_format(filename, store):
    if not os.path.exists(filename):
        raise FileNotFoundError(f'`{filename}` does not exist')
    dname = os.path.dirname(os.path.realpath(filename))
    store['dir'] = dname
    name = os.path.splitext(os.path.basename(filename))[0]
    if importlib.util.find_spec('mutagen') is None:
        raise OSError('python3 module `mutagen` is not installed')
    try:
        flac = FLAC(os.path.realpath(filename))
        store['flac'] = flac
        store['duration'] = flac.info.total_samples / flac.info.sample_rate
    except MutagenError:
        store['flac'] = None
    cue = f'{os.path.join(dname, name)}.cue'
    if os.path.exists(cue):
        store['cue'] = cue
    else:
        store['cue'] = None
        store['cuefile'] = cue
