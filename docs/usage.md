# Usage Examples

## `basename` – Extract filename from path

```bash
python basename.py /usr/bin/sort          # outputs: sort
python basename.py include/stdio.h .h     # outputs: stdio
python basename.py -a file1.txt file2.c   # outputs: file1 file2
```

## `mkdir` – Create directories

```bash
python mkdir.py newdir                    # simple directory
python mkdir.py -p a/b/c/d                # nested structure
python mkdir.py -m 755 newdir             # numeric permissions
python mkdir.py -m u=rwx,g=rx,o=r newdir  # symbolic permissions
```

## `rm` – Remove files and directories

```bash
python rm.py file.txt                     # remove a file
python rm.py -f missing.txt               # ignore missing files
python rm.py -i file.txt                  # prompt before removal
python rm.py -r dir/                      # recursively remove directory
python rm.py -rf dir/                     # force recursive removal
python rm.py --                           # treat following args as files, not options
python rm.py --help                       # show help information
```

## `date` – Print or set the system date and time

```bash
python date.py                            # print current date/time (matches GNU date)
python date.py '+%Y-%m-%d %H:%M:%S'       # custom format
python date.py -d '2024-01-01 12:00:00'   # parse date string
python date.py -r file.txt                # show mtime of file.txt
python date.py -u                         # UTC output
python date.py -I                         # ISO 8601 output
python date.py --rfc-3339 seconds         # RFC 3339 output
python date.py -R                         # RFC 5322 (email) output
python date.py --help                     # show help information
```

## `pwd` – Print current directory

```bash
python pwd.py                             # print current directory (physical, default)
python pwd.py -L                          # logical mode (uses $PWD if valid)
python pwd.py -P                          # physical mode (resolves symlinks)
python pwd.py --help                      # show help information
```

## `touch` – Update file timestamps

```bash
python touch.py file.txt                  # create or update
python touch.py -d "2 hours ago" file     # set relative time
python touch.py -r ref.txt file           # copy timestamp
python touch.py -t 202501011200 file      # exact datetime
```

## `echo` – Display a line of text

```bash
python echo.py "Hello World"              # Hello World
python echo.py -n "No newline"            # No newline (no trailing newline)
python echo.py -e "Line 1\nLine 2"        # Line 1 followed by Line 2 on new line
python echo.py -e "Tab\there"             # Tab    here
python echo.py -e "Bell\a"                # Bell (might trigger a terminal beep)
python echo.py -e "Stop here\cIgnored"    # Stop here (output stops at \c)
python echo.py -e "\x41\x42\x43"          # ABC (hex codes)
python echo.py -e "\101\102\103"          # ABC (octal codes)
```

## `whoami` – Print current user name

```bash
python whoami.py                          # outputs current username
python whoami.py --help                   # show help information
python whoami.py --version                # show version information
```
