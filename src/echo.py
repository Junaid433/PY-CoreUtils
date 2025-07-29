#!/usr/bin/env python3
"""
echo -- display a line of text
Python port of GNU coreutils echo
"""

import os
import sys

DEFAULT_ECHO_TO_XPG = False

def hextobin(c):
    """Convert hexadecimal character to integer."""
    if '0' <= c <= '9':
        return ord(c) - ord('0')
    elif c in 'aA':
        return 10
    elif c in 'bB':
        return 11
    elif c in 'cC':
        return 12
    elif c in 'dD':
        return 13
    elif c in 'eE':
        return 14
    elif c in 'fF':
        return 15
    else:
        return ord(c) - ord('0')
    
def is_hex_digit(c):
    """Check if character is a hexadecimal digit."""
    return ('0' <= c <= '9') or ('a' <= c.lower() <= 'f')

def process_escapes(s):
    r"""
    Process backslash escape sequences in string s.
    Returns (processed_string, should_continue)
    where should_continue is False if \c was encountered.
    """
    result = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
            next_char = s[i + 1]
            i += 2  
            
            if next_char == 'a':
                result.append('\a') 
            elif next_char == 'b':
                result.append('\b')  
            elif next_char == 'c':
                return ''.join(result), False  
            elif next_char == 'e':
                result.append('\x1B') 
            elif next_char == 'f':
                result.append('\f')  
            elif next_char == 'n':
                result.append('\n')  
            elif next_char == 'r':
                result.append('\r')  
            elif next_char == 't':
                result.append('\t') 
            elif next_char == 'v':
                result.append('\v') 
            elif next_char == 'x':
                if i < len(s) and is_hex_digit(s[i]):
                    hex_val = hextobin(s[i])
                    i += 1
                    if i < len(s) and is_hex_digit(s[i]):
                        hex_val = hex_val * 16 + hextobin(s[i])
                        i += 1
                    result.append(chr(hex_val))
                else:
                    result.append('\\')
                    result.append('x')
            elif next_char == '0':
                octal_val = 0
                if i < len(s) and '0' <= s[i] <= '7':
                    octal_val = ord(s[i]) - ord('0')
                    i += 1
                    if i < len(s) and '0' <= s[i] <= '7':
                        octal_val = octal_val * 8 + (ord(s[i]) - ord('0'))
                        i += 1
                        if i < len(s) and '0' <= s[i] <= '7':
                            octal_val = octal_val * 8 + (ord(s[i]) - ord('0'))
                            i += 1
                result.append(chr(octal_val))
            elif '1' <= next_char <= '7':
                octal_val = ord(next_char) - ord('0')
                if i < len(s) and '0' <= s[i] <= '7':
                    octal_val = octal_val * 8 + (ord(s[i]) - ord('0'))
                    i += 1
                    if i < len(s) and '0' <= s[i] <= '7':
                        octal_val = octal_val * 8 + (ord(s[i]) - ord('0'))
                        i += 1
                result.append(chr(octal_val))
            elif next_char == '\\':
                result.append('\\') 
            else:
                result.append('\\')
                i -= 1  
        else:
            result.append(c)
            i += 1
    
    return ''.join(result), True


def usage():
    """Print usage information."""
    program_name = os.path.basename(sys.argv[0])
    
    print(f"Usage: {program_name} [SHORT-OPTION]... [STRING]...")
    print(f"  or:  {program_name} LONG-OPTION")
    print()
    print("Echo the STRING(s) to standard output.")
    print()
    print("  -n             do not output the trailing newline")
    
    if DEFAULT_ECHO_TO_XPG:
        print("  -e             enable interpretation of backslash escapes (default)")
        print("  -E             disable interpretation of backslash escapes")
    else:
        print("  -e             enable interpretation of backslash escapes")
        print("  -E             disable interpretation of backslash escapes (default)")
    
    print("      --help     display this help and exit")
    print("      --version  output version information and exit")
    print()
    print("If -e is in effect, the following sequences are recognized:")
    print()
    print("  \\\\      backslash")
    print("  \\a      alert (BEL)")
    print("  \\b      backspace")
    print("  \\c      produce no further output")
    print("  \\e      escape")
    print("  \\f      form feed")
    print("  \\n      new line")
    print("  \\r      carriage return")
    print("  \\t      horizontal tab")
    print("  \\v      vertical tab")
    print("  \\0NNN   byte with octal value NNN (1 to 3 digits)")
    print("  \\xHH    byte with hexadecimal value HH (1 to 2 digits)")
    print()
    print("NOTE: your shell may have its own version of echo, which usually supersedes")
    print("the version described here. Please refer to your shell's documentation")
    print("for details about the options it supports.")
    print()
    print("Consider using the printf(1) command instead,")
    print("as it avoids problems when outputting option-like strings.")


def main():
    display_return = True
    posixly_correct = bool(os.getenv("POSIXLY_CORRECT"))
    
    allow_options = (not posixly_correct or 
                    (not DEFAULT_ECHO_TO_XPG and len(sys.argv) > 1 and sys.argv[1] == "-n"))
    
    do_v9 = DEFAULT_ECHO_TO_XPG
    
    if allow_options and len(sys.argv) == 2:
        if sys.argv[1] == "--help":
            usage()
            return 0
        elif sys.argv[1] == "--version":
            print("echo (Python port of GNU coreutils) 1.0")
            print("This is free software: you are free to change and redistribute it.")
            print("There is NO WARRANTY, to the extent permitted by law.")
            print("")
            print("Written by Junaid Rahman.")
            return 0
    
    args = sys.argv[1:]
    
    if allow_options:
        while args and args[0].startswith('-'):
            option = args[0]
            
            valid_option = True
            if len(option) == 1: 
                valid_option = False
            else:
                for char in option[1:]:
                    if char not in 'eEnN':
                        valid_option = False
                        break
            
            if not valid_option:
                break 
            
            for char in option[1:]:
                if char == 'e':
                    do_v9 = True
                elif char == 'E':
                    do_v9 = False
                elif char == 'n':
                    display_return = False
            
            args.pop(0)
    
    if do_v9 or posixly_correct:
        for i, arg in enumerate(args):
            processed_arg, should_continue = process_escapes(arg)
            sys.stdout.write(processed_arg)
            if not should_continue:
                return 0
            if i < len(args) - 1:
                sys.stdout.write(' ')
    else:
        for i, arg in enumerate(args):
            sys.stdout.write(arg)
            if i < len(args) - 1:
                sys.stdout.write(' ')
    
    if display_return:
        sys.stdout.write('\n')
    
    return 0


if __name__ == '__main__':
    sys.exit(main())