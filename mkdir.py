#!/usr/bin/env python3 

""""
mkdir - make directories
Python port of GNU coreutils mkdir
"""

import argparse
import os 
import stat
import sys 
from pathlib import Path

def parse_mode(mode_str):
    """
    Parse a mode string (like chmod) and return the numeric mode.
    Supports octal (755) and full symbolic (u+rwx,g+rx,o+rx) formats.
    """
    if not mode_str:
        return None
    
    if mode_str.isdigit() or (mode_str.startswith('0') and mode_str[1:].isdigit()):
        try:
            return int(mode_str, 8)
        except ValueError:
            return None
    
    current_mode = 0o777
    
    USER_BITS = {'r': 0o400, 'w': 0o200, 'x': 0o100}
    GROUP_BITS = {'r': 0o040, 'w': 0o020, 'x': 0o010}
    OTHER_BITS = {'r': 0o004, 'w': 0o002, 'x': 0o001}
    SPECIAL_BITS = {'s': 0o4000, 't': 0o1000}
    
    clauses = mode_str.split(',')
    
    for clause in clauses:
        clause = clause.strip()
        if not clause:
            continue
            
        who_chars = []
        i = 0
        while i < len(clause) and clause[i] in 'ugoa':
            who_chars.append(clause[i])
            i += 1
        
        if not who_chars:
            who_chars = ['a']
        
        if i >= len(clause):
            return None
        op = clause[i]
        if op not in '+-=':
            return None
        i += 1
        
        perms = clause[i:]
        if not perms:
            return None
        
        perm_bits = 0
        
        for perm in perms:
            if perm == 'r':
                if 'u' in who_chars or 'a' in who_chars:
                    perm_bits |= USER_BITS['r']
                if 'g' in who_chars or 'a' in who_chars:
                    perm_bits |= GROUP_BITS['r']
                if 'o' in who_chars or 'a' in who_chars:
                    perm_bits |= OTHER_BITS['r']
            elif perm == 'w':
                if 'u' in who_chars or 'a' in who_chars:
                    perm_bits |= USER_BITS['w']
                if 'g' in who_chars or 'a' in who_chars:
                    perm_bits |= GROUP_BITS['w']
                if 'o' in who_chars or 'a' in who_chars:
                    perm_bits |= OTHER_BITS['w']
            elif perm == 'x':
                if 'u' in who_chars or 'a' in who_chars:
                    perm_bits |= USER_BITS['x']
                if 'g' in who_chars or 'a' in who_chars:
                    perm_bits |= GROUP_BITS['x']
                if 'o' in who_chars or 'a' in who_chars:
                    perm_bits |= OTHER_BITS['x']
            elif perm == 's':
                if 'u' in who_chars or 'a' in who_chars:
                    perm_bits |= 0o4000  
                if 'g' in who_chars or 'a' in who_chars:
                    perm_bits |= 0o2000 
            elif perm == 't':
                if 'o' in who_chars or 'a' in who_chars:
                    perm_bits |= 0o1000 
            else:
                return None 
        
        if op == '+':
            current_mode |= perm_bits
        elif op == '-':
            current_mode &= ~perm_bits
        elif op == '=':
            mask = 0
            if 'u' in who_chars or 'a' in who_chars:
                mask |= 0o700 
            if 'g' in who_chars or 'a' in who_chars:
                mask |= 0o070 
            if 'o' in who_chars or 'a' in who_chars:
                mask |= 0o007
            current_mode &= ~mask
            current_mode |= perm_bits
    
    return current_mode

def make_directory(path, mode=None, parents=False, verbose=False, exists_ok=False):
    """
    Create a directory with specified mode.
    
    Args:
        path: Directory path to create
        mode: File mode (permissions) as integer
        parents: Create parent directories if needed
        verbose: Print messages for created directories
        exist_ok: Don't error if directory already exists
    
    Returns:
        True if successful, False otherwise
    """
    try:
        if parents:
            parent_path = os.path.dirname(path)
            if parent_path and parent_path != path and not os.path.exists(parent_path):
                make_directory(parent_path, parents=True, verbose=verbose, exists_ok=True)
        
        if mode is not None:
            old_umask = os.umask(0)
            try:
                os.mkdir(path, mode)
            finally:
                os.umask(old_umask)
        else:
            os.mkdir(path)
        
        if verbose:
            print(f'mkdir: created directory {path}')
        return True

    except FileExistsError:
        if exists_ok or parents:
            if os.path.isdir(path):
                return True
            else:
                print(f'mkdir: cannot create directory {path}: File exists.', file=sys.stderr)
                return False
        else:
            print(f"mkdir: cannot create directory '{path}': File exists", file=sys.stderr)
            return False
        
    except FileNotFoundError:
        if not parents:
            print(f"mkdir: cannot create directory '{path}': No such file or directory", file=sys.stderr)
        else:
            print(f"mkdir: cannot create directory '{path}': No such file or directory", file=sys.stderr)
        return False
    
    except PermissionError:
        print(f"mkdir: cannot create directory '{path}': Permission denied", file=sys.stderr)
        return False
    
    except OSError as e:
        print(f"mkdir: cannot create directory '{path}': {e.strerror}", file=sys.stderr)
        return False

def process_directories(directories, mode=None, parents=False, verbose=False, context=None):
    """
    Process multiple directories for creation.
    
    Returns:
        0 on success, 1 on any failure
    """
    success = True
    
    for directory in directories:
        if not make_directory(directory, mode=mode, parents=parents, verbose=verbose):
            success = False

        if context and verbose:
            print(f'mkdir: context support not implemented in this port')
    
    return 0 if success else 1

def main():
    parser = argparse.ArgumentParser(
        prog='mkdir',
        description='Create the DIRECTORY(ies), if they do not already exist.',
        add_help=False
    )
    
    parser.add_argument('-m', '--mode', metavar='MODE',
                       help='set file mode (as in chmod), not a=rwx - umask')
    parser.add_argument('-p', '--parents', action='store_true',
                       help='no error if existing, make parent directories as needed, '
                            'with their file modes unaffected by any -m option')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='print a message for each created directory')
    parser.add_argument('-Z', dest='context_default', action='store_true',
                       help='set SELinux security context of each created directory '
                            'to the default type')
    parser.add_argument('--context', metavar='CTX', nargs='?', const='default',
                       help='like -Z, or if CTX is specified then set the SELinux '
                            'or SMACK security context to CTX')
    parser.add_argument('--help', action='store_true',
                       help='display this help and exit')
    parser.add_argument('--version', action='store_true',
                       help='output version information and exit')
    parser.add_argument('directories', nargs='*', metavar='DIRECTORY',
                       help='directories to create')
    
    try:
        args = parser.parse_args()
    except SystemExit:
        return 1
    
    if args.help:
        print(f"""Usage: {parser.prog} [OPTION]... DIRECTORY...

Create the DIRECTORY(ies), if they do not already exist.

  -m, --mode=MODE   set file mode (as in chmod), not a=rwx - umask
  -p, --parents     no error if existing, make parent directories as needed,
                    with their file modes unaffected by any -m option
  -v, --verbose     print a message for each created directory
  -Z                   set SELinux security context of each created directory
                         to the default type
      --context[=CTX]  like -Z, or if CTX is specified then set the SELinux
                         or SMACK security context to CTX
      --help           display this help and exit
      --version        output version information and exit

Examples:
  {parser.prog} newdir              Create directory 'newdir'
  {parser.prog} -p a/b/c/d          Create directory tree 'a/b/c/d'
  {parser.prog} -m 755 newdir       Create 'newdir' with specific permissions
  {parser.prog} -pv /tmp/a/b/c      Create with parents and verbose output
""")
        return 0
    
    if args.version:
        print("mkdir (Python port of GNU coreutils) 1.0")
        print("This is free software: you are free to change and redistribute it.")
        print("There is NO WARRANTY, to the extent permitted by law.")
        print("")
        print("Written by Junaid Rahman.")
        return 0
    
    if not args.directories:
        print("mkdir: missing operand", file=sys.stderr)
        print(f"Try '{parser.prog} --help' for more information.", file=sys.stderr)
        return 1
    
    mode = None
    if args.mode:
        mode = parse_mode(args.mode)
        if mode is None:
            print(f"mkdir: invalid mode '{args.mode}'", file=sys.stderr)
            return 1
    
    context = None
    if args.context_default or args.context:
        context = args.context if args.context != 'default' else None
        if not args.verbose:
            print("mkdir: warning: SELinux/SMACK context support not implemented in this port", 
                  file=sys.stderr)
    
    return process_directories(
        args.directories,
        mode=mode,
        parents=args.parents,
        verbose=args.verbose,
        context=context
    )


if __name__ == '__main__':
    sys.exit(main())