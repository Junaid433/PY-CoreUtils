#!/usr/bin/env python3
"""
kill - send signals to processes, or list signals
Python port of GNU coreutils kill (carbon copy)
"""

import sys
import os
import signal
import argparse

# Build signal name/number maps (no SIG_*, no duplicates)
SIGNALS = {name: num for name, num in signal.__dict__.items()
           if name.startswith('SIG') and not name.startswith('SIG_') and isinstance(num, int)}
SIGNAL_NAMES = {num: name for name, num in SIGNALS.items()}
SIGNALS = {k: v for k, v in SIGNALS.items() if SIGNAL_NAMES[v] == k}


def parse_signal(sigstr):
    """
    Parse a signal name or number, return signal number or None if invalid.
    Accepts names with/without SIG prefix, or numbers.
    """
    if sigstr.isdigit():
        return int(sigstr)
    name = sigstr.upper()
    if name.startswith('SIG'):
        name = name[3:]
    return SIGNALS.get(f'SIG{name}')


def list_signals(args=None, number_mode=False, table=False):
    siglist = sorted((num, name) for name, num in SIGNALS.items())
    if table:
        num_width = max(len(str(num)) for num, _ in siglist)
        name_width = max(len(name) for _, name in siglist)
        for num, name in siglist:
            desc = signal.strsignal(num) if hasattr(signal, 'strsignal') else ''
            print(f"{num:>{num_width}} {name:<{name_width}} {desc}")
        return 0
    if args:
        for arg in args:
            if number_mode or arg.isdigit():
                try:
                    num = int(arg)
                except Exception:
                    print(f"kill: invalid signal number '{arg}'", file=sys.stderr)
                    return 1
                name = SIGNAL_NAMES.get(num)
                if name:
                    print(name)
                else:
                    print(f"kill: unknown signal '{arg}'", file=sys.stderr)
                    return 1
            else:
                sig = parse_signal(arg)
                if sig is not None:
                    print(sig)
                else:
                    print(f"kill: unknown signal '{arg}'", file=sys.stderr)
                    return 1
        return 0
    print(' '.join(name for _, name in siglist))
    return 0


def send_signals(signum, pids, prog):
    status = 0
    for pidstr in pids:
        try:
            pid = int(pidstr)
        except Exception:
            print(f"{prog}: {pidstr}: invalid process id", file=sys.stderr)
            status = 1
            continue
        try:
            os.kill(pid, signum)
        except ValueError:
            print(f"{prog}: {signum}: invalid signal", file=sys.stderr)
            status = 1
        except ProcessLookupError:
            print(f"{prog}: {pid}: no such process", file=sys.stderr)
            status = 1
        except PermissionError:
            print(f"{prog}: {pid}: permission denied", file=sys.stderr)
            status = 1
        except Exception as e:
            print(f"{prog}: {pid}: {e}", file=sys.stderr)
            status = 1
    return status


def print_help():
    print("kill: kill [-s sigspec | -n signum | -sigspec] pid | jobspec ... or kill -l [sigspec]\n")
    print("Send a signal to a job.\n")
    print("Send the processes identified by PID or JOBSPEC the signal named by\n")
    print("SIGSPEC or SIGNUM. If neither SIGSPEC nor SIGNUM is present, then\n")
    print("SIGTERM is assumed.\n")
    print("Options:\n")
    print("-s sig    SIG is a signal name\n")
    print("-n sig    SIG is a signal number\n")
    print("-l        list the signal names; if arguments follow `-l' they are\n")
    print("          assumed to be signal numbers for which names should be listed\n")
    print("-L        synonym for -l\n")
    print("-t        print a table of signal information\n")
    print("      --help     display this help and exit\n")
    print("      --version  output version information and exit\n")
    print("\nKill is a shell builtin for two reasons: it allows job IDs to be used\n")
    print("instead of process IDs, and allows processes to be killed if the limit\n")
    print("on processes that you can create is reached.\n")
    print("\nExit Status:\n")
    print("Returns success unless an invalid option is given or an error occurs.\n")


def print_version():
    print("kill (Python port of GNU coreutils) 1.0")
    print("This is free software: you are free to change and redistribute it.")
    print("There is NO WARRANTY, to the extent permitted by law.")
    print()
    print("Written by Junaid Rahman.")


def main():
    parser = argparse.ArgumentParser(
        prog='kill',
        description='Send signals to processes, or list signals.',
        add_help=False
    )
    parser.add_argument('-s', metavar='SIG', dest='signal_name', help='SIG is a signal name')
    parser.add_argument('-n', metavar='SIG', dest='signal_number', help='SIG is a signal number')
    parser.add_argument('-l', nargs='*', metavar='SIGSPEC', dest='list_signals', help='list signal names; if arguments follow, they are assumed to be signal numbers for which names should be listed')
    parser.add_argument('-L', nargs='*', metavar='SIGSPEC', dest='list_signals_L', help='synonym for -l')
    parser.add_argument('-t', action='store_true', dest='table', help='print a table of signal information')
    parser.add_argument('--help', action='store_true', help='display this help and exit')
    parser.add_argument('--version', action='store_true', help='output version information and exit')
    parser.add_argument('args', nargs=argparse.REMAINDER, help='PID(s) or signal spec')

    # Preprocess -SIGNAL (e.g., -9, -HUP, -SIGKILL) as -s SIGNAL,
    # but do NOT rewrite documented options (-l, -L, -t, -s, -n, --help, --version)
    argv = sys.argv[1:]
    new_argv = []
    signal_opt = None
    documented_opts = {'-l', '-L', '-t', '-s', '-n', '--help', '--version'}
    for arg in argv:
        if (
            arg.startswith('-') and len(arg) > 1 and not arg.startswith('--')
            and arg not in documented_opts
        ):
            # Accept -9, -KILL, -SIGKILL, etc. (but not documented options)
            signal_opt = arg[1:]
        else:
            new_argv.append(arg)
    if signal_opt:
        new_argv = ['-s', signal_opt] + new_argv
    args = parser.parse_args(new_argv)

    # Enforce mutual exclusion: only one of -s, -n, -l, -L, -t
    options = [bool(args.signal_name), bool(args.signal_number), args.list_signals is not None, args.list_signals_L is not None, args.table]
    if sum(options) > 1:
        print("kill: multiple signal/list/table options specified", file=sys.stderr)
        return 1

    if args.help:
        print_help()
        return 0
    if args.version:
        print_version()
        return 0

    # Handle -l and -L (list signals)
    if args.list_signals is not None or args.list_signals_L is not None:
        list_args = args.list_signals if args.list_signals is not None else args.list_signals_L
        return list_signals(args=list_args, number_mode=True if list_args else False)

    # Handle -t (table)
    if args.table:
        return list_signals(table=True)

    # Handle -s and -n
    signum = None
    if args.signal_name:
        signum = parse_signal(args.signal_name)
        if signum is None:
            print(f"kill: unknown signal '{args.signal_name}'", file=sys.stderr)
            return 1
    elif args.signal_number:
        if args.signal_number.isdigit():
            signum = int(args.signal_number)
        else:
            print(f"kill: invalid signal number '{args.signal_number}'", file=sys.stderr)
            return 1
    else:
        signum = signal.SIGTERM

    # Remaining args are PIDs
    pids = args.args
    if not pids:
        print(f"kill: missing operand", file=sys.stderr)
        print(f"Try 'kill --help' for more information.", file=sys.stderr)
        return 1
    return send_signals(signum, pids, 'kill')

if __name__ == '__main__':
    sys.exit(main())
