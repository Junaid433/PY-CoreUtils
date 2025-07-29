#!/usr/bin/env python3
"""
rm - Remove (unlink) files and directories
Python port of GNU coreutils rm
"""

import argparse
import os
import sys
import shutil
import stat

def is_root_path(path):
    return os.path.abspath(path) == os.path.sep

def prompt(msg):
    try:
        return input(msg).strip().lower().startswith('y')
    except EOFError:
        return False

def remove_file(path, force=False, interactive=None, verbose=False, dir_mode=False):
    try:
        if interactive == 'always':
            if not prompt(f"rm: remove regular file '{path}'? "):
                return True
        os.remove(path)
        if verbose:
            print(f"removed '{path}'")
        return True
    except FileNotFoundError:
        if not force:
            print(f"rm: cannot remove '{path}': No such file or directory", file=sys.stderr)
            return False
        return True
    except IsADirectoryError:
        if dir_mode:
            return remove_dir(path, force, interactive, verbose, recursive=False)
        print(f"rm: cannot remove '{path}': Is a directory", file=sys.stderr)
        return False
    except PermissionError:
        print(f"rm: cannot remove '{path}': Permission denied", file=sys.stderr)
        return False
    except Exception as e:
        print(f"rm: cannot remove '{path}': {e}", file=sys.stderr)
        return False

def remove_dir(path, force=False, interactive=None, verbose=False, recursive=False, preserve_root=True):
    if is_root_path(path) and preserve_root:
        print("rm: it is dangerous to operate recursively on '/'", file=sys.stderr)
        print("rm: use --no-preserve-root to override this failsafe", file=sys.stderr)
        return False
    if interactive == 'always':
        if not prompt(f"rm: remove directory '{path}'? "):
            return True
    if recursive:
        try:
            if interactive == 'once':
                if not prompt(f"rm: descend into directory '{path}'? "):
                    return True
            shutil.rmtree(path, onerror=lambda func, p, exc: None if force else (_ for _ in ()).throw(exc[1]))
            if verbose:
                print(f"removed directory '{path}'")
            return True
        except FileNotFoundError:
            if not force:
                print(f"rm: cannot remove '{path}': No such file or directory", file=sys.stderr)
                return False
            return True
        except Exception as e:
            print(f"rm: cannot remove '{path}': {e}", file=sys.stderr)
            return False
    else:
        try:
            os.rmdir(path)
            if verbose:
                print(f"removed directory '{path}'")
            return True
        except OSError as e:
            if not force:
                print(f"rm: cannot remove '{path}': {e.strerror}", file=sys.stderr)
                return False
            return True

def main():
    parser = argparse.ArgumentParser(
        prog="rm",
        description="Remove (unlink) the FILE(s).",
        add_help=False
    )
    parser.add_argument('-f', '--force', action='store_true', help='ignore nonexistent files and arguments, never prompt')
    parser.add_argument('-i', action='store_true', help='prompt before every removal')
    parser.add_argument('-I', action='store_true', help='prompt once before removing more than three files, or when removing recursively')
    parser.add_argument('--interactive', nargs='?', choices=['never', 'once', 'always'], const='always', help='prompt according to WHEN: never, once (-I), or always (-i); without WHEN, prompt always')
    parser.add_argument('--no-preserve-root', action='store_true', help='do not treat "/" specially')
    parser.add_argument('--preserve-root', nargs='?', const='default', help='do not remove "/" (default); with "all", reject any command line argument on a separate device from its parent (not fully implemented)')
    parser.add_argument('-r', '-R', '--recursive', action='store_true', help='remove directories and their contents recursively')
    parser.add_argument('-d', '--dir', action='store_true', help='remove empty directories')
    parser.add_argument('-v', '--verbose', action='store_true', help='explain what is being done')
    parser.add_argument('--help', action='store_true', help='display this help and exit')
    parser.add_argument('--version', action='store_true', help='output version information and exit')
    parser.add_argument('files', nargs='*', help='files or directories to remove')

    args = parser.parse_args()

    if args.help:
        parser.print_help()
        print("""
By default, rm does not remove directories. Use the --recursive (-r or -R)
option to remove each listed directory, too, along with all of its contents.

Any attempt to remove a file whose last file name component is '.' or '..'
is rejected with a diagnostic.

To remove a file whose name starts with a '-', for example '-foo',
use one of these commands:
  rm -- -foo
  rm ./-foo

If you use rm to remove a file, it might be possible to recover
some of its contents, given sufficient expertise and/or time. For greater
assurance that the contents are unrecoverable, consider using shred(1).
""")
        return 0
    if args.version:
        print("rm (Python port of GNU coreutils) 1.0")
        print("This is free software: you are free to change and redistribute it.")
        print("There is NO WARRANTY, to the extent permitted by law.")
        print("")
        print("Written by Junaid Rahman.")
        return 0

    if not args.files:
        if args.force:
            return 0
        print("rm: missing operand", file=sys.stderr)
        print("Try 'rm --help' for more information.", file=sys.stderr)
        return 1

    if args.i:
        interactive = 'always'
    elif args.I:
        interactive = 'once'
    elif args.interactive:
        interactive = args.interactive
    else:
        interactive = 'never' if args.force else ('always' if sys.stdin.isatty() else 'never')

    preserve_root = not args.no_preserve_root
    status = 0

    if interactive == 'once' and (args.recursive or len(args.files) > 3):
        msg = f"rm: remove {len(args.files)} {'arguments recursively' if args.recursive else 'arguments'}? "
        if not prompt(msg):
            return 0

    for path in args.files:
        if path in ('.', '..'):
            print(f"rm: refusing to remove '{path}' or parent directory", file=sys.stderr)
            status = 1
            continue
        try:
            st = os.lstat(path)
            if stat.S_ISDIR(st.st_mode):
                if args.recursive or args.dir:
                    ok = remove_dir(
                        path,
                        force=args.force,
                        interactive=interactive,
                        verbose=args.verbose,
                        recursive=args.recursive,
                        preserve_root=preserve_root
                    )
                else:
                    print(f"rm: cannot remove '{path}': Is a directory", file=sys.stderr)
                    ok = False
            else:
                ok = remove_file(
                    path,
                    force=args.force,
                    interactive=interactive,
                    verbose=args.verbose,
                    dir_mode=args.dir
                )
            if not ok:
                status = 1
        except FileNotFoundError:
            if not args.force:
                print(f"rm: cannot remove '{path}': No such file or directory", file=sys.stderr)
                status = 1
        except Exception as e:
            print(f"rm: error removing '{path}': {e}", file=sys.stderr)
            status = 1
    return status

if __name__ == '__main__':
    sys.exit(main())
