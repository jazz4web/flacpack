import argparse
import pprint
import sys

from .checker import check_format
from .parser import export_metadata, extract_metadata, read_file


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
        extract_metadata(meta, arguments.filename)
        export_metadata(meta)
    else:
        pass
    pprint.pprint(meta)
