import argparse
import pprint
import re
import sys

from .checker import check_format
from .parser import parse_field, read_file


def parse_args(version):
    args = argparse.ArgumentParser()
    args.add_argument(
        '-v', '--version', action='version', version=version)
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
    print(arguments)
    meta = dict()
    check_format(arguments.filename, meta)
    if meta['cue']:
        read_file(meta)
        parse_field(
            re.compile(r'FILE +(.+)'), arguments.filename, meta['cuecont'])
    else:
        pass
    pprint.pprint(meta)
