#!/usr/bin/env python3
"""
uptime - tell how long the system has been running
Python port of GNU coreutils uptime
"""

import argparse
import os
import re
import struct
import subprocess
import sys
import time
from datetime import datetime

# --- Constants and helpers from users.py for user counting ---
DEFAULT_UTMP_FILE = '/var/run/utmp'
USER_PROCESS = 7
UTMP_STRUCT_FORMAT = 'hi32s4s32s256shhiii4i20x'
UTMP_STRUCT_SIZE = struct.calcsize(UTMP_STRUCT_FORMAT)


def get_user_count_unix(filename):
    """Reads a utmp-like file and counts active user sessions."""
    count = 0
    try:
        with open(filename, 'rb') as f:
            while True:
                record = f.read(UTMP_STRUCT_SIZE)
                if not record or len(record) < UTMP_STRUCT_SIZE:
                    break
                unpacked_record = struct.unpack(UTMP_STRUCT_FORMAT, record)
                if unpacked_record[0] == USER_PROCESS:
                    username = unpacked_record[4].split(b'\0', 1)[0]
                    if username:
                        count += 1
    except (FileNotFoundError, PermissionError, IOError):
        # Errors are handled gracefully, returning 0 users
        pass
    return count


def get_user_count_windows():
    """Gets user count on Windows by parsing 'query user' output."""
    try:
        result = subprocess.run(['query', 'user'], capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore')
        # Count non-header lines that contain a username
        return len([line for line in result.stdout.strip().split('\n')[1:] if re.match(r'\s*>?(\S+)', line)])
    except (FileNotFoundError, subprocess.CalledProcessError):
        return 1  # Fallback to 1 user if query fails


def get_user_count(filename):
    """Platform-aware function to get the number of logged-in users."""
    if sys.platform.startswith('linux') or sys.platform == 'darwin':
        return get_user_count_unix(filename)
    elif sys.platform == 'win32':
        return get_user_count_windows()
    return 0


def get_boot_time():
    """Returns the system boot time as a Unix timestamp."""
    if sys.platform.startswith('linux'):
        try:
            # Allow overriding the path for testing purposes
            proc_stat_path = os.environ.get('_PYCOREUTILS_TEST_PROC_STAT', '/proc/stat')
            with open(proc_stat_path) as f:
                for line in f:
                    if line.startswith('btime'):
                        return float(line.split()[1])
        except (FileNotFoundError, IndexError, ValueError):
            return None
    elif sys.platform == 'darwin':
        try:
            result = subprocess.run(['sysctl', '-n', 'kern.boottime'], capture_output=True, text=True, check=True)
            match = re.search(r'sec\s*=\s*(\d+)', result.stdout)
            if match:
                return float(match.group(1))
        except (FileNotFoundError, subprocess.CalledProcessError, IndexError, ValueError):
            return None
    elif sys.platform == 'win32':
        try:
            result = subprocess.run(['wmic', 'os', 'get', 'lastbootuptime'], capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            boottime_str = result.stdout.strip().split('\n')[1].split('.')[0]
            dt_obj = datetime.strptime(boottime_str, '%Y%m%d%H%M%S')
            return dt_obj.timestamp()
        except (FileNotFoundError, subprocess.CalledProcessError, IndexError, ValueError):
            return None
    return None


def main():
    parser = argparse.ArgumentParser(
        prog='uptime',
        description='Print the current time, system uptime, user count, and load averages.',
        add_help=False
    )
    parser.add_argument('file', nargs='?', default=DEFAULT_UTMP_FILE,
                        help='file to read user information from (e.g., /var/log/wtmp)')
    parser.add_argument('--help', action='store_true', help='display this help and exit')
    parser.add_argument('--version', action='store_true', help='output version information and exit')

    args, unknown = parser.parse_known_args()

    if args.help:
        print(f"Usage: {parser.prog} [OPTION]... [FILE]")
        print("Print the current time, the length of time the system has been up,")
        print("the number of users on the system, and the average number of jobs")
        print("in the run queue over the last 1, 5 and 15 minutes.")
        print(f"\nIf FILE is not specified, use {DEFAULT_UTMP_FILE}. /var/log/wtmp as FILE is common.\n")
        print("      --help     display this help and exit")
        print("      --version  output version information and exit")
        return 0

    if args.version:
        print("uptime (Python port of GNU coreutils) 1.0")
        print("This is free software: you are free to change and redistribute it.")
        print("There is NO WARRANTY, to the extent permitted by law.")
        print("\nWritten by Junaid Rahman.")
        return 0

    if unknown:
        print(f"uptime: extra operand '{unknown[0]}'", file=sys.stderr)
        print(f"Try '{parser.prog} --help' for more information.", file=sys.stderr)
        return 1

    current_time_str = datetime.now().strftime('%H:%M:%S')

    boot_time = get_boot_time()
    uptime_str = "up ??:??"
    if boot_time:
        uptime_seconds = int(time.time() - boot_time)
        if uptime_seconds >= 0:
            up_days = uptime_seconds // 86400
            up_hours = (uptime_seconds % 86400) // 3600
            up_mins = (uptime_seconds % 3600) // 60
            if up_days > 0:
                day_str = "day" if up_days == 1 else "days"
                uptime_str = f"up {up_days} {day_str}, {up_hours:2}:{up_mins:02}"
            else:
                uptime_str = f"up {up_hours:2}:{up_mins:02}"

    user_count = get_user_count(args.file)
    user_str = f"{user_count} user" if user_count == 1 else f"{user_count} users"

    load_avg_str = ""
    if hasattr(os, 'getloadavg'):
        try:
            # Allow overriding load average for testing
            fake_load = os.environ.get('_PYCOREUTILS_TEST_LOAD_AVG')
            if fake_load:
                avg = [float(x) for x in fake_load.split(',')]
            else:
                avg = os.getloadavg()
            load_avg_str = f",  load average: {avg[0]:.2f}, {avg[1]:.2f}, {avg[2]:.2f}"
        except OSError:
            pass

    print(f" {current_time_str} {uptime_str},  {user_str}{load_avg_str}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
