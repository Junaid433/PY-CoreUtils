#!/usr/bin/env python3
"""
hostid - print the hexadecimal identifier for the current host
Python port of GNU coreutils hostid
"""

import argparse
import os
import sys

def get_host_id():
    """
    Get the host ID using several methods to ensure cross-platform compatibility.

    1. Try os.gethostid() if available.
    2. Try reading the binary ID from /etc/hostid.
    3. Fallback to using the host's primary IP address.

    Returns the host ID as an integer or None if all methods fail.
    """
    # Method 1: Use os.gethostid() if available.
    if hasattr(os, 'gethostid'):
        try:
            return os.gethostid()
        except OSError:
            # Function exists but is not implemented by the underlying C library.
            pass

    # Method 2: Read from the common /etc/hostid file.
    try:
        with open('/etc/hostid', 'rb') as f:
            import struct
            host_id_bytes = f.read(4)
            if len(host_id_bytes) == 4:
                # Unpack 4 bytes as a little-endian unsigned integer.
                return struct.unpack('<I', host_id_bytes)[0]
    except (FileNotFoundError, IOError):
        pass

    # Method 3: Fallback to deriving from the host's IP address.
    try:
        import socket
        import struct
        ip_address = socket.gethostbyname(socket.gethostname())
        # The IP address is already in network byte order (big-endian).
        return struct.unpack('!I', socket.inet_aton(ip_address))[0]
    except Exception:
        pass

    return None

def main():
    parser = argparse.ArgumentParser(
        prog='hostid',
        description='Print the numeric identifier (in hexadecimal) for the current host.',
        add_help=False
    )

    parser.add_argument('--help', action='store_true',
                       help='display this help and exit')
    parser.add_argument('--version', action='store_true',
                       help='output version information and exit')

    args, unknown = parser.parse_known_args()

    if args.help:
        print(f"Usage: {parser.prog} [OPTION]")
        print("Print the numeric identifier (in hexadecimal) for the current host.")
        print()
        print("      --help     display this help and exit")
        print("      --version  output version information and exit")
        return 0

    if args.version:
        print("hostid (Python port of GNU coreutils) 1.0")
        print("This is free software: you are free to change and redistribute it.")
        print("There is NO WARRANTY, to the extent permitted by law.")
        print()
        print("Written by Junaid Rahman.")
        return 0

    if unknown:
        print(f"hostid: extra operand '{unknown[0]}'", file=sys.stderr)
        print(f"Try '{parser.prog} --help' for more information.", file=sys.stderr)
        return 1

    host_id = get_host_id()

    if host_id is None:
        print(f"hostid: cannot get host id: no method succeeded", file=sys.stderr)
        return 1

    # The C code does `id &= 0xffffffff;` to handle potential sign-extension.
    # We mimic this behavior for consistency and to ensure a 32-bit result.
    host_id &= 0xffffffff

    print(f"{host_id:08x}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
