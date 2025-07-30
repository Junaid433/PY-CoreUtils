#!/usr/bin/env python3
"""
id - print real and effective user and group IDs
Python port of GNU coreutils id
"""

import argparse
import os
import pwd
import grp
import sys

ok = True

def get_user_by_spec(spec):
    """
    Get user info (pwd struct) from a username or UID string.
    Returns (pwd_struct, error_message).
    """
    try:
        if spec.isdigit():
            uid = int(spec)
            return pwd.getpwuid(uid), None
        else:
            return pwd.getpwnam(spec), None
    except (KeyError, ValueError):
        return None, f"id: '{spec}': no such user"

def print_id(id_val, id_type, use_name):
    """
    Prints a user or group ID, optionally resolving it to a name.
    id_type should be 'user' or 'group'.
    """
    global ok
    name = None
    if use_name:
        try:
            if id_type == 'user':
                name = pwd.getpwuid(id_val).pw_name
            else:  # group
                name = grp.getgrgid(id_val).gr_name
        except KeyError:
            # GNU id doesn't print an error here, it just prints the number.
            pass
            ok = False
    
    if name:
        print(name, end='')
    else:
        print(id_val, end='')

def print_group_list(username, use_name, delimiter):
    """
    Prints all group IDs for a given user or the current process.
    """
    global ok
    try:
        if username:
            user_info = pwd.getpwnam(username)
            # os.getgrouplist includes the user's primary group ID
            groups = sorted(os.getgrouplist(username, user_info.pw_gid))
        else:  # current process
            # For the current process, get real, effective, and supplementary
            groups = sorted(list(set([os.getgid(), os.getegid()] + os.getgroups())))
    except (KeyError, OSError) as e:
        err_user = f" for user {username}" if username else ""
        print(f"id: failed to get groups{err_user}: {e}", file=sys.stderr)
        ok = False
        return

    output = []
    for g in groups:
        if use_name:
            try:
                output.append(grp.getgrgid(g).gr_name)
            except KeyError:
                output.append(str(g)) # Fallback to number if name not found
        else:
            output.append(str(g))

    print(delimiter.join(output), end='')

def print_full_info(ruid, euid, rgid, egid, username=None):
    """
    Prints the default, full user and group information.
    """
    global ok
    try:
        print(f"uid={ruid}({pwd.getpwuid(ruid).pw_name})", end='')
        print(f" gid={rgid}({grp.getgrgid(rgid).gr_name})", end='')

        if euid != ruid:
            print(f" euid={euid}({pwd.getpwuid(euid).pw_name})", end='')
        if egid != rgid:
            print(f" egid={egid}({grp.getgrgid(egid).gr_name})", end='')
    except KeyError as e:
        # This can happen if a UID/GID doesn't have a corresponding name
        print(f"\nid: cannot find name for ID {e.args[0]}", file=sys.stderr)
        ok = False
        return

    try:
        if username:
            user_info = pwd.getpwnam(username)
            all_groups = sorted(os.getgrouplist(username, user_info.pw_gid))
        else:
            all_groups = sorted(list(set([rgid, egid] + os.getgroups())))

        if all_groups:
            group_strings = []
            for gid in all_groups:
                try:
                    g_name = grp.getgrgid(gid).gr_name
                    group_strings.append(f"{gid}({g_name})")
                except KeyError:
                    group_strings.append(str(gid))

            print(f" groups={','.join(group_strings)}", end='')
    except (KeyError, OSError) as e:
        err_user = f" for user {username}" if username else ""
        print(f"\nid: failed to get groups{err_user}: {e}", file=sys.stderr)
        ok = False

def main():
    def do_print_for_ids(args, ruid, euid, rgid, egid, username=None):
        """Helper to perform the printing action."""
        delimiter = '\0' if args.zero else ' '

        if args.user:
            uid_to_print = ruid if args.real else euid
            print_id(uid_to_print, 'user', args.name)
        elif args.group:
            gid_to_print = rgid if args.real else egid
            print_id(gid_to_print, 'group', args.name)
        elif args.groups:
            print_group_list(username, args.name, delimiter)
        else: # default format
            print_full_info(ruid, euid, rgid, egid, username)

    global ok
    parser = argparse.ArgumentParser(
        prog='id',
        description='Print user and group information for the specified USER, or (when USER is omitted) for the current user.',
        add_help=False
    )
    parser.add_argument('-a', action='store_true', help='ignore, for compatibility')
    parser.add_argument('-Z', '--context', action='store_true', help='print only the security context of the process')
    parser.add_argument('-g', '--group', action='store_true', help='print only the effective group ID')
    parser.add_argument('-G', '--groups', action='store_true', help='print all group IDs')
    parser.add_argument('-n', '--name', action='store_true', help='print a name instead of a number, for -u, -g, -G')
    parser.add_argument('-r', '--real', action='store_true', help='print the real ID instead of the effective ID, with -u, -g, -G')
    parser.add_argument('-u', '--user', action='store_true', help='print only the effective user ID')
    parser.add_argument('-z', '--zero', action='store_true', help='delimit entries with NUL characters, not whitespace')
    parser.add_argument('--help', action='store_true', help='display this help and exit')
    parser.add_argument('--version', action='store_true', help='output version information and exit')
    parser.add_argument('users', nargs='*', metavar='USER', help='user to inspect')

    args = parser.parse_args()

    if args.help:
        print(f"Usage: {parser.prog} [OPTION]... [USER]")
        print("Print user and group information for each specified USER, or (when USER is omitted) for the current user.")
        print("\n  -a             ignore, for compatibility with other versions\n  -Z, --context  print only the security context of the process (not supported)\n  -g, --group    print only the effective group ID\n  -G, --groups   print all group IDs\n  -n, --name     print a name instead of a number, for -u,-g,-G\n  -r, --real     print the real ID instead of the effective ID, with -u,-g,-G\n  -u, --user     print only the effective user ID\n  -z, --zero     delimit entries with NUL characters, not whitespace;\n                   not permitted in default format")
        print("      --help     display this help and exit\n      --version  output version information and exit")
        print("\nWithout any OPTION, print some useful set of identified information.")
        return 0

    if args.version:
        print("id (Python port of GNU coreutils) 1.0\nThis is free software: you are free to change and redistribute it.\nThere is NO WARRANTY, to the extent permitted by law.\n\nWritten by Junaid Rahman.")
        return 0

    if sum([args.user, args.group, args.groups, args.context]) > 1:
        print("id: cannot print 'only' of more than one choice", file=sys.stderr)
        return 1
    if not any([args.user, args.group, args.groups, args.context]) and (args.name or args.real):
        print("id: cannot print only names or real IDs in default format", file=sys.stderr)
        return 1
    if not any([args.user, args.group, args.groups, args.context]) and args.zero:
        print("id: option --zero not permitted in default format", file=sys.stderr)
        return 1
    if args.users and args.context:
        print("id: cannot print security context when user specified", file=sys.stderr)
        return 1

    if args.context:
        print("id: --context not supported in this port", file=sys.stderr)
        return 1

    end_char = '\0' if args.zero else '\n'

    if args.users:
        for user_spec in args.users:
            user_info, err_msg = get_user_by_spec(user_spec)
            if err_msg:
                print(err_msg, file=sys.stderr)
                ok = False
                continue

            ruid = euid = user_info.pw_uid
            rgid = egid = user_info.pw_gid
            username = user_info.pw_name
            do_print_for_ids(args, ruid, euid, rgid, egid, username)
            print(end_char, end='')
    else:
        try:
            ruid = os.getuid()
            euid = os.geteuid()
            rgid = os.getgid()
            egid = os.getegid()
            do_print_for_ids(args, ruid, euid, rgid, egid, None)
            print(end_char, end='')
        except OSError as e:
            print(f"id: cannot get IDs: {e}", file=sys.stderr)
            return 1

    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
