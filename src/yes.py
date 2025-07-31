#!/usr/bin/env python3
"""
yes - output a string repeatedly until killed
Python port of GNU coreutils yes
"""

import sys
import os
import signal

def main():
    """
    Main function to handle argument parsing and execution.
    """
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help':
            print("Usage: yes [STRING]...")
            print("  or:  yes OPTION")
            print("\nRepeatedly output a line with all specified STRING(s), or 'y'.\n")
            print("      --help     display this help and exit")
            print("      --version  output version information and exit")
            return 0
        if sys.argv[1] == '--version':
            print("yes (Python port of GNU coreutils) 1.0")
            print("This is free software: you are free to change and redistribute it.")
            print("There is NO WARRANTY, to the extent permitted by law.")
            print("\nWritten by Junaid Rahman.")
            return 0

    # If arguments are provided, join them. Otherwise, default to 'y'.
    if len(sys.argv) > 1:
        output_string = ' '.join(sys.argv[1:]) + '\n'
    else:
        output_string = 'y\n'

    # On UNIX-like systems, restore the default SIGPIPE handler.
    # This makes the script terminate silently when its output pipe is closed,
    # which is the standard behavior for CLI tools like this.
    if sys.platform != "win32":
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    try:
        while True:
            sys.stdout.write(output_string)
    except KeyboardInterrupt:
        # Gracefully exit on Ctrl-C.
        return 0
    except IOError as e:
        # This will catch other I/O errors, but not BrokenPipeError on UNIX
        # because of the SIGPIPE handler above.
        print(f"yes: standard output: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
