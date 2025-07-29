#!/usr/bin/env python3
"""
pwd - print current directory
Python port of GNU coreutils pwd
"""
import argparse
import os
import sys
import locale

def logical_getcwd():
    wd = os.environ.get('PWD')
    if not wd or not wd.startswith('/'):
        return None
    p = wd
    while True:
        idx = p.find('/.')
        if idx == -1:
            break
        if len(p) > idx+2 and (p[idx+2] == '/' or p[idx+2] == '' or (p[idx+2] == '.' and (len(p) == idx+3 or p[idx+3] == '/'))):
            return None
        p = p[idx+2:]
    try:
        st1 = os.stat(wd)
        st2 = os.stat('.')
        if (st1.st_ino, st1.st_dev) == (st2.st_ino, st2.st_dev):
            return wd
    except Exception:
        pass
    return None

def main():
    parser = argparse.ArgumentParser(
        prog="pwd",
        description="Print the full filename of the current working directory.",
        add_help=False
    )
    parser.add_argument('-L', '--logical', action='store_true', help='use PWD from environment, even if it contains symlinks')
    parser.add_argument('-P', '--physical', action='store_true', help='avoid all symlinks')
    parser.add_argument('--help', action='store_true', help='display this help and exit')
    parser.add_argument('--version', action='store_true', help='output version information and exit')
    parser.add_argument('args', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    args = parser.parse_args()

    if args.help:
        parser.print_help()
        print("""
-L, --logical   use PWD from environment, even if it contains symlinks
-P, --physical  avoid all symlinks
If no option is specified, -P is assumed (unless POSIXLY_CORRECT is set, then -L).
""")
        return 0
    if args.version:
        print("pwd (Python port of GNU coreutils) 1.0")
        print("This is free software: you are free to change and redistribute it.")
        print("There is NO WARRANTY, to the extent permitted by law.")
        print("")
        print("Written by Junaid Rahman.")
        return 0
    
    if args.args:
        print("pwd: ignoring non-option arguments", file=sys.stderr)

    logical = bool(os.environ.get('POSIXLY_CORRECT', None))
    if args.logical:
        logical = True
    if args.physical:
        logical = False

    if logical:
        wd = logical_getcwd()
        if wd:
            print(wd)
            return 0
    try:
        wd = os.path.realpath(os.getcwd())
        print(wd)
        return 0
    except Exception as e:
        print(f"pwd: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
