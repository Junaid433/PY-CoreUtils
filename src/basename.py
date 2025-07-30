#!/usr/bin/env python3 
""""
basename - Strip directory and suffix from file names
Python port of GNU coreutils basename 
"""

import argparse
import os 
import sys 
from pathlib import Path

def remove_suffix(name, suffix):
    """
    Remove Suffix from the end of name if it is there, unless name consists entirely of suffix.
    """
    if not suffix or len(name) <= len(suffix):
        return name

    if name.endswith(suffix):
        if len(name) == len(suffix):
            return name 
        return name[:-len(suffix)]
    
    return name

def strip_trailing_slashes(path):
    """
    Strip trailing slashes from path, but preserve root indicators.
    """
    if path in ('/', '\\') or (len(path) == 3 and path[1:] == ':\\'):
        return path 

    return path.rstrip('/\\')

def is_absolute_path(path):
    """
    Check if path is absolute or a drive letter.
    """
    return os.path.isabs(path) or (len(path) == 2 and path[1] == ':')

def get_file_system_prefix_len(path):
    """"
    Get length of file system prefix (drive letter on Windows)
    """
    if len(path) >= 2 and path[1] == ':':
        return 2 
    
    return 0

def base_name(path):
    """
    Extract the base name from a path, similar to C basename().
    """
    if not path:
        return '.'
    if path == '/':
        return '/'
    if path == '//':
        return '//'
    
    path = strip_trailing_slashes(path)

    if len(path) == 2 and path[1] == ':':
        return path
    
    return os.path.basename(path)

def perform_basename(string, suffix, use_nuls):
    """
    Perform the basename operation on string. If suffix is non-null, remove
    the trailing suffix. Finally, output the result string.
    """
    name = base_name(string)
    
    if suffix and not is_absolute_path(string) and not get_file_system_prefix_len(name):
        name = remove_suffix(name, suffix)

    if use_nuls:
        sys.stdout.write(name + '\0')
    else:
        print(name)

def main():
    parser = argparse.ArgumentParser(
        prog='basename',
        description='Print NAME with any leading directory components removed. '
                   'If specified, also remove a trailing SUFFIX.',
        add_help=False 
    )
    
    parser.add_argument('-a', '--multiple', action='store_true',
                       help='support multiple arguments and treat each as a NAME')
    parser.add_argument('-s', '--suffix', metavar='SUFFIX',
                       help='remove a trailing SUFFIX; implies -a')
    parser.add_argument('-z', '--zero', action='store_true',
                       help='end each output line with NUL, not newline')
    parser.add_argument('--help', action='store_true',
                       help='display this help and exit')
    parser.add_argument('--version', action='store_true',
                       help='output version information and exit')
    parser.add_argument('names', nargs='*', help='NAME [SUFFIX]')
    
    try:
        args = parser.parse_args()
    except SystemExit:
        return 1
    
    if args.help:
        print(f"""Usage: {parser.prog} NAME [SUFFIX]
  or:  {parser.prog} OPTION... NAME...

Print NAME with any leading directory components removed.
If specified, also remove a trailing SUFFIX.

  -a, --multiple       support multiple arguments and treat each as a NAME
  -s, --suffix=SUFFIX  remove a trailing SUFFIX; implies -a
  -z, --zero           end each output line with NUL, not newline
      --help           display this help and exit
      --version        output version information and exit

Examples:
  {parser.prog} /usr/bin/sort          -> "sort"
  {parser.prog} include/stdio.h .h     -> "stdio"
  {parser.prog} -s .h include/stdio.h  -> "stdio"
  {parser.prog} -a any/str1 any/str2   -> "str1" followed by "str2"
""")
        return 0
    
    if args.version:
        print("basename (Python port of GNU coreutils) 1.0")
        print("This is free software: you are free to change and redistribute it.")
        print("There is NO WARRANTY, to the extent permitted by law.")
        print("")
        print("Written by Junaid Rahman.")
        return 0
    
    multiple_names = args.multiple or args.suffix is not None
    suffix = args.suffix
    use_nuls = args.zero
    
    if not args.names:
        print("basename: missing operand", file=sys.stderr)
        print(f"Try '{parser.prog} --help' for more information.", file=sys.stderr)
        return 1
    
    if not multiple_names and len(args.names) > 2:
        print(f"basename: extra operand '{args.names[2]}'", file=sys.stderr)
        print(f"Try '{parser.prog} --help' for more information.", file=sys.stderr)
        return 1
    
    if multiple_names:
        for name in args.names:
            perform_basename(name, suffix, use_nuls)
    else:
        name = args.names[0]
        single_suffix = args.names[1] if len(args.names) == 2 else None
        perform_basename(name, single_suffix, use_nuls)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())