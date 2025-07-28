#!/usr/bin/env python3
"""
touch -- change modification and access times of files
Python port of GNU coreutils touch
"""

import argparse
import os
import sys
import time
import stat
from datetime import datetime
from pathlib import Path
import re


CH_ATIME = 1
CH_MTIME = 2


def parse_posix_time(time_str):
    """
    Parse POSIX time format: [[CC]YY]MMDDhhmm[.ss]
    Returns timestamp or None if invalid.
    """
    clean_str = time_str.replace('.', '')
    
    if not clean_str.isdigit():
        return None
    
    if len(clean_str) == 8: 
        month = int(clean_str[:2])
        day = int(clean_str[2:4])
        hour = int(clean_str[4:6])
        minute = int(clean_str[6:8])
        year = datetime.now().year
        second = 0
    elif len(clean_str) == 10:  
        if '.' in time_str:  
            parts = time_str.split('.')
            if len(parts[0]) == 8 and len(parts[1]) == 2:
                month = int(parts[0][:2])
                day = int(parts[0][2:4])
                hour = int(parts[0][4:6])
                minute = int(parts[0][6:8])
                second = int(parts[1])
                year = datetime.now().year
            else:
                return None
        else:  
            year = int(clean_str[:2])
            if year < 70:
                year += 2000
            else:
                year += 1900
            month = int(clean_str[2:4])
            day = int(clean_str[4:6])
            hour = int(clean_str[6:8])
            minute = int(clean_str[8:10])
            second = 0
    elif len(clean_str) == 12: 
        if '.' in time_str: 
            parts = time_str.split('.')
            if len(parts[0]) == 10 and len(parts[1]) == 2:
                year = int(parts[0][:2])
                if year < 70:
                    year += 2000
                else:
                    year += 1900
                month = int(parts[0][2:4])
                day = int(parts[0][4:6])
                hour = int(parts[0][6:8])
                minute = int(parts[0][8:10])
                second = int(parts[1])
            else:
                return None
        else:  
            year = int(clean_str[:4])
            month = int(clean_str[4:6])
            day = int(clean_str[6:8])
            hour = int(clean_str[8:10])
            minute = int(clean_str[10:12])
            second = 0
    elif len(clean_str) == 14: 
        if '.' in time_str: 
            parts = time_str.split('.')
            if len(parts[0]) == 12 and len(parts[1]) == 2:
                year = int(parts[0][:4])
                month = int(parts[0][4:6])
                day = int(parts[0][6:8])
                hour = int(parts[0][8:10])
                minute = int(parts[0][10:12])
                second = int(parts[1])
            else:
                return None
        else:
            year = int(clean_str[:4])
            month = int(clean_str[4:6])
            day = int(clean_str[6:8])
            hour = int(clean_str[8:10])
            minute = int(clean_str[10:12])
            second = int(clean_str[12:14])
    else:
        return None
    
    if not (1 <= month <= 12 and 1 <= day <= 31 and 0 <= hour <= 23 and 
            0 <= minute <= 59 and 0 <= second <= 59):
        return None
    
    try:
        dt = datetime(year, month, day, hour, minute, second)
        return dt.timestamp()
    except ValueError:
        return None


def parse_date_string(date_str):
    """
    Parse a date string in various formats.
    This is a simplified version - the real GNU date parser is much more complex.
    """
    if not date_str:
        return None
    
    if date_str.lower() == 'now':
        return time.time()
    
    if 'ago' in date_str.lower():
        if 'hour' in date_str:
            match = re.search(r'(\d+)\s+hour', date_str)
            if match:
                hours = int(match.group(1))
                return time.time() - (hours * 3600)
        elif 'day' in date_str:
            match = re.search(r'(\d+)\s+day', date_str)
            if match:
                days = int(match.group(1))
                return time.time() - (days * 86400)
    
    try:
        dt = datetime.fromisoformat(date_str.replace('T', ' '))
        return dt.timestamp()
    except ValueError:
        pass
    
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d',
        '%m/%d/%Y %H:%M:%S',
        '%m/%d/%Y %H:%M',
        '%m/%d/%Y',
        '%d %b %Y %H:%M:%S',
        '%d %b %Y %H:%M',
        '%d %b %Y',
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.timestamp()
        except ValueError:
            continue
    
    return None


def touch_file(filepath, atime=None, mtime=None, no_create=False, no_dereference=False):
    """
    Touch a file, updating its access and/or modification times.
    
    Args:
        filepath: Path to the file
        atime: Access time (timestamp) or None to use current time
        mtime: Modification time (timestamp) or None to use current time
        no_create: Don't create file if it doesn't exist
        no_dereference: Don't follow symlinks
    
    Returns:
        True if successful, False otherwise
    """
    try:
        if filepath == "-":
            return True
        
        path = Path(filepath)
        
        if no_dereference:
            exists = path.is_symlink() or path.exists()
        else:
            exists = path.exists()
        
        if not exists:
            if no_create:
                return True
            else:
                try:
                    path.touch()
                except (OSError, IOError) as e:
                    print(f"touch: cannot touch '{filepath}': {e.strerror}", file=sys.stderr)
                    return False
        
        current_time = time.time()
        access_time = atime if atime is not None else current_time
        mod_time = mtime if mtime is not None else current_time
        
        if no_dereference and path.is_symlink():
            if atime is not None or mtime is not None:
                print(f"touch: warning: cannot change times of symlink '{filepath}' (not supported in Python port)", file=sys.stderr)
            return True
        else:
            os.utime(filepath, (access_time, mod_time))
        
        return True
        
    except (OSError, IOError) as e:
        if no_create and e.errno == 2: 
            return True
        print(f"touch: setting times of '{filepath}': {e.strerror}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"touch: cannot touch '{filepath}': {str(e)}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        prog='touch',
        description='Update the access and modification times of each FILE to the current time.\n\n'
                   'A FILE argument that does not exist is created empty, unless -c or -h is supplied.\n\n'
                   'A FILE argument string of - is handled specially and causes touch to '
                   'change the times of the file associated with standard output.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False
    )
    
    parser.add_argument('-a', action='store_true',
                       help='change only the access time')
    parser.add_argument('-c', '--no-create', action='store_true',
                       help='do not create any files')
    parser.add_argument('-d', '--date', metavar='STRING',
                       help='parse STRING and use it instead of current time')
    parser.add_argument('-f', action='store_true',
                       help='(ignored)')
    parser.add_argument('-h', '--no-dereference', action='store_true',
                       help='affect each symbolic link instead of any referenced file '
                            '(useful only on systems that can change the timestamps of a symlink)')
    parser.add_argument('-m', action='store_true',
                       help='change only the modification time')
    parser.add_argument('-r', '--reference', metavar='FILE',
                       help="use this file's times instead of current time")
    parser.add_argument('-t', metavar='STAMP',
                       help='use [[CC]YY]MMDDhhmm[.ss] instead of current time')
    parser.add_argument('--time', choices=['atime', 'access', 'use', 'mtime', 'modify'],
                       help='specify which time to change: access time (-a): "access", "atime", "use"; '
                            'modification time (-m): "modify", "mtime"')
    parser.add_argument('--help', action='store_true',
                       help='display this help and exit')
    parser.add_argument('--version', action='store_true',
                       help='output version information and exit')
    parser.add_argument('files', nargs='*', metavar='FILE',
                       help='files to touch')
    
    try:
        args = parser.parse_args()
    except SystemExit:
        return 1
    
    if args.help:
        print(f"""Usage: {parser.prog} [OPTION]... FILE...

Update the access and modification times of each FILE to the current time.

A FILE argument that does not exist is created empty, unless -c or -h
is supplied.

A FILE argument string of - is handled specially and causes touch to
change the times of the file associated with standard output.

  -a                     change only the access time
  -c, --no-create        do not create any files
  -d, --date=STRING      parse STRING and use it instead of current time
  -f                     (ignored)
  -h, --no-dereference   affect each symbolic link instead of any referenced
                         file (useful only on systems that can change the
                         timestamps of a symlink)
  -m                     change only the modification time
  -r, --reference=FILE   use this file's times instead of current time
  -t STAMP               use [[CC]YY]MMDDhhmm[.ss] instead of current time
      --time=WORD        specify which time to change:
                           access time (-a): 'access', 'atime', 'use';
                           modification time (-m): 'modify', 'mtime'
      --help             display this help and exit
      --version          output version information and exit

Examples:
  {parser.prog} file               Create 'file' or update its time to now
  {parser.prog} -c file            Don't create 'file' if it doesn't exist
  {parser.prog} -d "2 hours ago" f Set time to 2 hours ago
  {parser.prog} -r ref_file file   Use ref_file's times for file
  {parser.prog} -t 202501011200 f  Set time to Jan 1, 2025 12:00
""")
        return 0
    
    if args.version:
        print("touch (Python port of GNU coreutils) 1.0")
        print("This is free software: you are free to change and redistribute it.")
        print("There is NO WARRANTY, to the extent permitted by law.")
        print("")
        print("Written by Junaid Rahman.")
        return 0
    
    if not args.files:
        print("touch: missing file operand", file=sys.stderr)
        print(f"Try '{parser.prog} --help' for more information.", file=sys.stderr)
        return 1
    
    change_times = 0
    if args.a:
        change_times |= CH_ATIME
    if args.m:
        change_times |= CH_MTIME
    if args.time:
        if args.time in ['atime', 'access', 'use']:
            change_times |= CH_ATIME
        elif args.time in ['mtime', 'modify']:
            change_times |= CH_MTIME
    
    if change_times == 0:
        change_times = CH_ATIME | CH_MTIME
    
    time_sources = sum([bool(args.date), bool(args.reference), bool(args.t)])
    if time_sources > 1:
        print("touch: cannot specify times from more than one source", file=sys.stderr)
        return 1
    
    target_time = None
    if args.reference:
        try:
            ref_stat = os.stat(args.reference)
            if change_times & CH_ATIME:
                atime = ref_stat.st_atime
            else:
                atime = None
            if change_times & CH_MTIME:
                mtime = ref_stat.st_mtime
            else:
                mtime = None
            target_time = (atime, mtime)
        except (OSError, IOError) as e:
            print(f"touch: failed to get attributes of '{args.reference}': {e.strerror}", file=sys.stderr)
            return 1
    elif args.t:
        timestamp = parse_posix_time(args.t)
        if timestamp is None:
            print(f"touch: invalid date format '{args.t}'", file=sys.stderr)
            return 1
        if change_times & CH_ATIME:
            atime = timestamp
        else:
            atime = None
        if change_times & CH_MTIME:
            mtime = timestamp
        else:
            mtime = None
        target_time = (atime, mtime)
    elif args.date:
        timestamp = parse_date_string(args.date)
        if timestamp is None:
            print(f"touch: invalid date format '{args.date}'", file=sys.stderr)
            return 1
        if change_times & CH_ATIME:
            atime = timestamp
        else:
            atime = None
        if change_times & CH_MTIME:
            mtime = timestamp
        else:
            mtime = None
        target_time = (atime, mtime)
    
    success = True
    for filepath in args.files:
        if target_time:
            atime, mtime = target_time
        else:
            current = time.time()
            atime = current if (change_times & CH_ATIME) else None
            mtime = current if (change_times & CH_MTIME) else None
        
        if not touch_file(filepath, atime=atime, mtime=mtime, 
                         no_create=args.no_create, no_dereference=args.no_dereference):
            success = False
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())