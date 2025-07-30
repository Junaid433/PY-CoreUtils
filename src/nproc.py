#!/usr/bin/env python3
"""
nproc -- print the number of processors
Python port of GNU coreutils nproc
"""

import os
import sys

def usage(status):
    program_name = os.path.basename(sys.argv[0])
    if status != 0:
        print(f"Try '{program_name} --help' for more information.", file=sys.stderr)
    else:
        print(f"Usage: {program_name} [OPTION]...\n")
        print("Print the number of processing units available to the current process,\n"
              "which may be less than the number of online processors\n\n")
        print("  --all         print the number of installed processors")
        print("  --ignore=N    if possible, exclude N processing units")
        print("      --help     display this help and exit")
        print("      --version  output version information and exit\n")
        print("Written by Giuseppe Scrivano.")
    sys.exit(status)


def error(msg, arg=None):
    program_name = os.path.basename(sys.argv[0])
    if arg is not None:
        print(f"{program_name}: {msg} {arg}", file=sys.stderr)
    else:
        print(f"{program_name}: {msg}", file=sys.stderr)

def parse_ignore(optarg):
    try:
        n = int(optarg)
        if n < 0:
            raise ValueError
        return n
    except Exception:
        error("invalid number", repr(optarg))
        usage(1)


def num_processors(mode):
    if mode == 'all':
        try:
            return os.cpu_count() or 1
        except Exception:
            return 1
    else:
        try:
            if hasattr(os, 'sched_getaffinity'):
                return len(os.sched_getaffinity(0))
        except Exception:
            pass
        try:
            return os.cpu_count() or 1
        except Exception:
            return 1


def main():
    args = sys.argv[1:]
    mode = 'current'
    ignore = 0

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == '--help':
            usage(0)
        elif arg == '--version':
            print("nproc (Python port of GNU coreutils) 1.0")
            print("This is free software: you are free to change and redistribute it.")
            print("There is NO WARRANTY, to the extent permitted by law.")
            print("")
            print("Written by Junaid Rahman.")
            return 0
        elif arg == '--all':
            mode = 'all'
            i += 1
        elif arg.startswith('--ignore='):
            ignore = parse_ignore(arg.split('=', 1)[1])
            i += 1
        elif arg == '--ignore':
            if i + 1 >= len(args):
                error("option '--ignore' requires an argument")
                usage(1)
            ignore = parse_ignore(args[i + 1])
            i += 2
        elif arg.startswith('-'):
            error(f"unrecognized option '{arg}'")
            usage(1)
        else:
            break
    if i < len(args):
        error("extra operand", repr(args[i]))
        usage(1)

    nproc = num_processors(mode)
    if ignore < nproc:
        nproc -= ignore
    else:
        nproc = 1
    print(f"{nproc}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
