#!/usr/bin/env python3
"""
users - print the user names of users currently logged in
Python port of GNU coreutils users
"""

import argparse
import os
import struct
import re
import sys
import subprocess

DEFAULT_UTMP_FILE = '/var/run/utmp'
USER_PROCESS = 7
UTMP_STRUCT_FORMAT = 'hi32s4s32s256shhiii4i20x'
UTMP_STRUCT_SIZE = struct.calcsize(UTMP_STRUCT_FORMAT)

def get_logged_in_users_unix(filename):
    """
    Reads a utmp-like file and returns a sorted list of all logged-in user sessions.

    Args:
        filename (str): The path to the utmp file.

    Returns:
        list: A sorted list of usernames, with duplicates for multiple sessions.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be read.
        IOError: For other I/O related errors.
    """
    users = []
    with open(filename, 'rb') as f:
        while True:
            record = f.read(UTMP_STRUCT_SIZE)
            if not record:
                break
            if len(record) < UTMP_STRUCT_SIZE:
                continue

            unpacked_record = struct.unpack(UTMP_STRUCT_FORMAT, record)
            ut_type = unpacked_record[0]
            
            if ut_type == USER_PROCESS:
                ut_user_bytes = unpacked_record[4]
                username = ut_user_bytes.split(b'\0', 1)[0].decode('utf-8', 'ignore')
                if username:
                    users.append(username)
    
    return sorted(users)

def get_logged_in_users_windows():
    """
    Gets logged-in users on Windows by parsing the output of 'query user'.
    Falls back to os.getlogin() if 'query user' is unavailable.
    """
    users = []
    try:
        # The 'query user' command lists logged-in users on Windows.
        result = subprocess.run(['query', 'user'], capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore')
        lines = result.stdout.strip().split('\n')
        # Skip the header line
        for line in lines[1:]:
            # The first word is the username. It might start with '>' for the current session.
            match = re.match(r'\s*>?(\S+)', line)
            if match:
                users.append(match.group(1))
    except (FileNotFoundError, subprocess.CalledProcessError):
        try:
            users.append(os.getlogin())
        except OSError:
            users.append(os.environ.get('USERNAME', 'unknown'))
            
    return sorted(users)

def get_logged_in_users(filename):
    """
    Platform-aware function to get logged-in users.
    """
    if sys.platform.startswith('linux') or sys.platform == 'darwin':
        return get_logged_in_users_unix(filename)
    elif sys.platform == 'win32':
        return get_logged_in_users_windows()
    else:
        return [os.getlogin()] if hasattr(os, 'getlogin') else []

def main():
    """
    Main function to handle argument parsing and execution.
    """
    parser = argparse.ArgumentParser(
        prog='users',
        description='Output who is currently logged in according to FILE.',
        epilog=f"If FILE is not specified, use {DEFAULT_UTMP_FILE}. /var/log/wtmp as FILE is common.",
        add_help=False
    )
    parser.add_argument('file', nargs='?', default=DEFAULT_UTMP_FILE,
                        help='the file to read user information from')
    parser.add_argument('--help', action='store_true',
                        help='display this help and exit')
    parser.add_argument('--version', action='store_true',
                        help='output version information and exit')
    
    args, unknown = parser.parse_known_args()

    if args.help:
        print(f"Usage: {parser.prog} [OPTION]... [FILE]")
        print("Output who is currently logged in according to FILE.")
        print(f"If FILE is not specified, use {DEFAULT_UTMP_FILE}. /var/log/wtmp as FILE is common.")
        print()
        print("      --help     display this help and exit")
        print("      --version  output version information and exit")
        return 0

    if args.version:
        print("users (Python port of GNU coreutils) 1.0")
        print("This is free software: you are free to change and redistribute it.")
        print("There is NO WARRANTY, to the extent permitted by law.")
        print()
        print("Written by Junaid Rahman.")
        return 0

    if unknown:
        print(f"users: extra operand '{unknown[0]}'", file=sys.stderr)
        print(f"Try '{parser.prog} --help' for more information.", file=sys.stderr)
        return 1

    if sys.platform == 'win32' and args.file != DEFAULT_UTMP_FILE:
        print("users: warning: FILE argument is ignored on Windows", file=sys.stderr)

    try:
        user_list = get_logged_in_users(args.file)
        if user_list:
            print(' '.join(user_list))
    except FileNotFoundError:
        if args.file != DEFAULT_UTMP_FILE:
            print(f"users: cannot open '{args.file}': No such file or directory", file=sys.stderr)
            return 1
    except PermissionError:
        print(f"users: cannot open '{args.file}': Permission denied", file=sys.stderr)
        return 1
    except (IOError, struct.error) as e:
        print(f"users: error reading '{args.file}': {e}", file=sys.stderr)
        return 1
        
    return 0

if __name__ == '__main__':
    sys.exit(main())