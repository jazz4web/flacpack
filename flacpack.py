#!/usr/bin/env python3

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

from flacpack import version
from flacpack.main import parse_args, show_error, start_the_process

try:
    start_the_process(parse_args(version))
except Exception as e:
    show_error(e)
