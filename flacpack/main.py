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

import argparse
import os
import sys

from .checker import check_format, check_pic
from .parser import (
    export_metadata, extract_metadata, import_cuesheet, read_file)


def parse_args(version):
    args = argparse.ArgumentParser()
    args.add_argument(
        '-v', '--version', action='version', version=version)
    args.add_argument(
        '-p', action='store', dest='pic', help='add a cover front picture')
    args.add_argument(
        'filename', action='store', help='the target file name')
    return args.parse_args()


def show_error(msg, code=1):
    print(
        os.path.basename(sys.argv[0]),
        'error',
        msg,
        sep=':',
        file=sys.stderr)
    sys.exit(code)


def start_the_process(arguments):
    meta = dict()
    check_format(arguments.filename, meta)
    if arguments.pic and meta.get('cue'):
        check_pic(arguments, meta)
    if meta['flac'] is None:
        raise FileNotFoundError('cannot find FLAC file')
    if meta['cue']:
        read_file(meta)
        extract_metadata(meta, os.path.basename(arguments.filename))
        export_metadata(meta)
    else:
        import_cuesheet(meta, os.path.basename(arguments.filename))
