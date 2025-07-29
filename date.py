#!/usr/bin/env python3
"""
date - print or set the system date and time
Python port of GNU coreutils date
"""

import argparse
import os
import sys
import time
import locale
from datetime import datetime, timezone, timedelta

try:
    from dateutil import parser as dateutil_parser
except ImportError:
    dateutil_parser = None

def parse_date_string(s):
    if dateutil_parser:
        try:
            return dateutil_parser.parse(s)
        except Exception:
            return None
    fmts = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M",
        "%m/%d/%Y",
        "%d %b %Y %H:%M:%S",
        "%d %b %Y %H:%M",
        "%d %b %Y",
        "%a, %d %b %Y %H:%M:%S %z",
        "%a %b %d %H:%M:%S %Z %Y",
    ]
    for fmt in fmts:
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            continue
    return None

def get_file_mtime(path):
    st = os.stat(path)
    return datetime.fromtimestamp(st.st_mtime)

def print_date(dt, fmt, use_utc=False, c_locale=False):
    if use_utc:
        dt = dt.astimezone(timezone.utc)
    if c_locale:
        locale.setlocale(locale.LC_TIME, 'C')
    import re
    out = dt.strftime(fmt)
    # For default format, trim +HH00 or -HH00 to +HH or -HH
    if fmt == "%a %b %d %I:%M:%S %p %z %Y":
        out = re.sub(r'([+-][0-9]{2})00 ', r'\1 ', out)
    print(out)
    if c_locale:
        locale.setlocale(locale.LC_TIME, '')

def main():
    parser = argparse.ArgumentParser(
        prog="date",
        description="Display or set the system date and time.",
        add_help=False
    )
    parser.add_argument('-d', '--date', metavar='STRING', help="display time described by STRING, not 'now'")
    parser.add_argument('-f', '--file', metavar='DATEFILE', help="like --date; once for each line of DATEFILE")
    parser.add_argument('-I', '--iso-8601', nargs='?', const='date', choices=['date', 'hours', 'minutes', 'seconds', 'ns'], help="output date/time in ISO 8601 format")
    parser.add_argument('--rfc-3339', metavar='FMT', choices=['date', 'seconds', 'ns'], help="output date/time in RFC 3339 format")
    parser.add_argument('-R', '--rfc-email', action='store_true', help="output date and time in RFC 5322 format")
    parser.add_argument('--rfc-822', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--rfc-2822', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('-r', '--reference', metavar='FILE', help="display the last modification time of FILE")
    parser.add_argument('-s', '--set', metavar='STRING', help="set time described by STRING")
    parser.add_argument('-u', '--utc', '--universal', action='store_true', help="print or set Coordinated Universal Time (UTC)")
    parser.add_argument('--help', action='store_true', help='display this help and exit')
    parser.add_argument('--version', action='store_true', help='output version information and exit')
    parser.add_argument('format', nargs='?', help="output format (starting with '+')")

    args = parser.parse_args()

    if args.help:
        parser.print_help()
        print("""
Usage: date [OPTION]... [+FORMAT]
  or:  date [-u|--utc|--universal] [MMDDhhmm[[CC]YY][.ss]]

Display date and time in the given FORMAT.
With -s, or with [MMDDhhmm[[CC]YY][.ss]], set the date and time.

-d, --date=STRING display time described by STRING, not 'now'
-f, --file=DATEFILE like --date; once for each line of DATEFILE
-I[FMT], --iso-8601[=FMT] output date/time in ISO 8601 format.
--rfc-3339=FMT output date/time in RFC 3339 format.
-R, --rfc-email output date and time in RFC 5322 format.
-r, --reference=FILE display the last modification time of FILE
-s, --set=STRING set time described by STRING
-u, --utc, --universal print or set Coordinated Universal Time (UTC)
--help display this help and exit
--version output version information and exit

FORMAT controls the output. Interpreted sequences are as in strftime(3).
""")
        return 0
    if args.version:
        print("date (Python port of GNU coreutils) 1.0")
        print("This is free software: you are free to change and redistribute it.")
        print("There is NO WARRANTY, to the extent permitted by law.")
        print("")
        print("Written by Junaid Rahman.")

    date_sources = [bool(args.date), bool(args.file), bool(args.reference)]
    if sum(date_sources) > 1:
        print("date: the options to specify dates for printing are mutually exclusive", file=sys.stderr)
        return 1
    if args.set and any(date_sources):
        print("date: the options to print and set the time may not be used together", file=sys.stderr)
        return 1

    dt = None
    if args.reference:
        try:
            dt = get_file_mtime(args.reference)
        except Exception as e:
            print(f"date: {e}", file=sys.stderr)
            return 1
    elif args.date:
        dt = parse_date_string(args.date)
        if not dt:
            print(f"date: invalid date '{args.date}'", file=sys.stderr)
            return 1
    elif args.file:
        try:
            with open(args.file) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    d = parse_date_string(line)
                    if not d:
                        print(f"date: invalid date '{line}'", file=sys.stderr)
                        continue
                    print_date(d, get_output_format(args), args.utc)
            return 0
        except Exception as e:
            print(f"date: {e}", file=sys.stderr)
            return 1
    elif args.set:
        print("date: setting the system clock is not supported in this Python port.", file=sys.stderr)
        dt = parse_date_string(args.set)
        if not dt:
            print(f"date: invalid date '{args.set}'", file=sys.stderr)
            return 1
    else:
        if args.utc:
            dt = datetime.now(timezone.utc)
        else:
            dt = datetime.now().astimezone()

    # Output
    fmt = get_output_format(args)
    c_locale = args.rfc_email or args.rfc_822 or args.rfc_2822
    print_date(dt, fmt, use_utc=args.utc, c_locale=c_locale)
    return 0

def get_output_format(args):
    if args.rfc_email or args.rfc_822 or args.rfc_2822:
        return "%a, %d %b %Y %H:%M:%S %z"
    if args.iso_8601:
        if args.iso_8601 == 'date':
            return "%Y-%m-%d"
        if args.iso_8601 == 'hours':
            return "%Y-%m-%dT%H%z"
        if args.iso_8601 == 'minutes':
            return "%Y-%m-%dT%H:%M%z"
        if args.iso_8601 == 'seconds':
            return "%Y-%m-%dT%H:%M:%S%z"
        if args.iso_8601 == 'ns':
            return "%Y-%m-%dT%H:%M:%S.%f%z"
    if args.rfc_3339:
        if args.rfc_3339 == 'date':
            return "%Y-%m-%d"
        if args.rfc_3339 == 'seconds':
            return "%Y-%m-%d %H:%M:%S%z"
        if args.rfc_3339 == 'ns':
            return "%Y-%m-%d %H:%M:%S.%f%z"
    if args.format and args.format.startswith('+'):
        return args.format[1:]
    return "%a %b %d %I:%M:%S %p %z %Y"

if __name__ == '__main__':
    sys.exit(main())
