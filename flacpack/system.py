import os
import shlex

from subprocess import Popen, PIPE


def check_dep(dependency):
    for path in os.getenv('PATH').split(':'):
        dep_bin = os.path.join(path, dependency)
        if os.path.exists(dep_bin):
            return True


def detect_c_type(name, text=True):
    dep = check_dep('file')
    if not dep:
        raise OSError(f'`file` is not installed')
    cmd = shlex.split(f'file -b --mime-type "{name}"')
    with Popen(cmd, stdout=PIPE, stderr=PIPE) as p:
        result = p.communicate()
    if p.returncode:
        raise RuntimeError('something bad happened')
    if text:
        if result[0].decode('utf-8').strip() != 'text/plain':
            raise ValueError('bad cue')
    else:
        if result[0].decode('utf-8').strip() != 'image/jpeg':
            raise ValueError('bad picture')
