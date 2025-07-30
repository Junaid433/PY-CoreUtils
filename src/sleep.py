#!/usr/bin/env python3
"""
sleep - pause for a specified amount of time
Python port of GNU coreutils sleep
"""

import sys
import os
import time
import argparse

def parse_time_interval(arg):
    """
    Parse a time interval argument, return seconds as float, or None if invalid.
    """
    if not arg:
        return None
    num_part = ''
    suffix = ''
    for i, c in enumerate(arg):
        if (c.isdigit() or c == '.' or (c == '-' and i == 0)):
            num_part += c
        else:
            suffix = arg[i:]
            break
    try:
        value = float(num_part)
    except ValueError:
        return None
    if not suffix:
        suffix_char = ''
    elif len(suffix) == 1:
        suffix_char = suffix
    else:
        return None
    if suffix_char in ('', 's'):
        return value
    elif suffix_char == 'm':
        return value * 60
    elif suffix_char == 'h':
        return value * 3600
    elif suffix_char == 'd':
        return value * 86400
    else:
        return None

def main():
    parser = argparse.ArgumentParser(
        prog='sleep',
        description='Pause for NUMBER seconds. SUFFIX may be s, m, h, or d. With multiple arguments, sum their values.',
        add_help=False
    )
    parser.add_argument('times', nargs='*', help='NUMBER[SUFFIX]...')
    parser.add_argument('--help', action='store_true', help='display this help and exit')
    parser.add_argument('--version', action='store_true', help='output version information and exit')

    args = parser.parse_args()

    if args.help:
        print(f"Usage: {parser.prog} NUMBER[SUFFIX]...")
        print(f"  or:  {parser.prog} OPTION")
        print()
        print("Pause for NUMBER seconds, where NUMBER is an integer or floating-point.")
        print("SUFFIX may be 's','m','h', or 'd', for seconds, minutes, hours, days.")
        print("With multiple arguments, pause for the sum of their values.")
        print()
        print("      --help     display this help and exit")
        print("      --version  output version information and exit")
        return 0
    if args.version:
        print("sleep (Python port of GNU coreutils) 1.0")
        print("This is free software: you are free to change and redistribute it.")
        print("There is NO WARRANTY, to the extent permitted by law.")
        print("")
        print("Written by Junaid Rahman.")
        return 0

    if not args.times:
        print(f"{parser.prog}: missing operand", file=sys.stderr)
        print(f"Try '{parser.prog} --help' for more information.", file=sys.stderr)
        return 1

    seconds = 0.0
    ok = True
    for arg in args.times:
        s = parse_time_interval(arg)
        if s is None or s < 0:
            print(f"{parser.prog}: invalid time interval '{arg}'", file=sys.stderr)
            ok = False
            continue
        seconds += s
    if not ok:
        return 1
    try:
        time.sleep(seconds)
    except Exception as e:
        print(f"{parser.prog}: cannot sleep: {e}", file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
