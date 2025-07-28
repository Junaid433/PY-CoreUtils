#!/usr/bin/env python3
"""
whoami - Print effective userid.
Python port of GNU coreutils whoami
"""

import sys
import os
import pwd
import argparse

def main():
    parser = argparse.ArgumentParser(
        prog='whoami',
        description="Print the user name associated with the current effective user ID. Same as id -un.",
        add_help=False 
    )
    
    parser.add_argument('--help', action='store_true',
                       help='display this help and exit')
    parser.add_argument('--version', action='store_true',
                       help='output version information and exit')
    
    args, unknown = parser.parse_known_args()
    
    if args.help:
        print("Usage: whoami [OPTION]...")
        print("Print the user name associated with the current effective user ID.")
        print("Same as id -un.")
        print()
        print("      --help     display this help and exit")
        print("      --version  output version information and exit")
        return 0
    
    if args.version:
        print("whoami (GNU coreutils) 9.7")
        print("Copyright (C) 2025 Free Software Foundation, Inc.")
        print("License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.")
        print("This is free software: you are free to change and redistribute it.")
        print("There is NO WARRANTY, to the extent permitted by law.")
        print()
        print("Written by Richard Mlynarik.")
        return 0
    
    if unknown:
        print(f"whoami: extra operand '{unknown[0]}'", file=sys.stderr)
        print("Try 'whoami --help' for more information.", file=sys.stderr)
        return 1
    
    try:
        uid = os.geteuid()
        pw_entry = pwd.getpwuid(uid)
        print(pw_entry.pw_name)
        return 0
        
    except KeyError:
        print(f"whoami: cannot find name for user ID {uid}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"whoami: cannot find name for user ID {uid}: {e.strerror if hasattr(e, 'strerror') else str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())