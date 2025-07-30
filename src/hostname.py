#!/usr/bin/env python3
"""
hostname - set or print the name of current host system
Python port of GNU coreutils hostname
"""

import argparse
import os
import socket
import sys

def main():
    """
    Main function to handle argument parsing and execution.
    """
    parser = argparse.ArgumentParser(
        prog='hostname',
        description='Print or set the hostname of the current system.',
        add_help=False
    )
    parser.add_argument('--help', action='store_true', help='display this help and exit')
    parser.add_argument('--version', action='store_true', help='output version information and exit')

    args, name_args = parser.parse_known_args()

    if args.help:
        print(f"Usage: {parser.prog} [NAME]")
        print(f"  or:  {parser.prog} OPTION")
        print("Print or set the hostname of the current system.")
        print()
        print("      --help     display this help and exit")
        print("      --version  output version information and exit")
        return 0

    if args.version:
        print("hostname (Python port of GNU coreutils) 1.0")
        print("This is free software: you are free to change and redistribute it.")
        print("There is NO WARRANTY, to the extent permitted by law.")
        print()
        print("Written by Junaid Rahman.")
        return 0

    if len(name_args) > 1:
        print(f"hostname: extra operand '{name_args[1]}'", file=sys.stderr)
        print(f"Try '{parser.prog} --help' for more information.", file=sys.stderr)
        return 1

    # Set hostname if an argument is provided
    if len(name_args) == 1:
        name_to_set = name_args[0]
        if not hasattr(os, 'sethostname'):
            print(f"hostname: cannot set name to '{name_to_set}': Function not implemented", file=sys.stderr)
            return 1
        try:
            os.sethostname(name_to_set)
        except PermissionError:
            print(f"hostname: cannot set name to '{name_to_set}': Operation not permitted", file=sys.stderr)
            return 1
        except OSError as e:
            print(f"hostname: cannot set name to '{name_to_set}': {e.strerror}", file=sys.stderr)
            return 1
    # Print hostname if no arguments are provided
    else:
        try:
            print(socket.gethostname())
        except socket.gaierror as e:
            print(f"hostname: cannot determine hostname: {e}", file=sys.stderr)
            return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
