# Usage Examples

## `basename` – Extract filename from path

```bash
python src/basename.py /usr/bin/sort          # outputs: sort
python src/basename.py include/stdio.h .h     # outputs: stdio
python src/basename.py -a file1.txt file2.c   # outputs: file1 file2
```

## `mkdir` – Create directories

```bash
python src/mkdir.py newdir                    # simple directory
python src/mkdir.py -p a/b/c/d                # nested structure
python src/mkdir.py -m 755 newdir             # numeric permissions
python src/mkdir.py -m u=rwx,g=rx,o=r newdir  # symbolic permissions
```

## `rm` – Remove files and directories

```bash
python src/rm.py file.txt                     # remove a file
python src/rm.py -f missing.txt               # ignore missing files
python src/rm.py -i file.txt                  # prompt before removal
python src/rm.py -r dir/                      # recursively remove directory
python src/rm.py -rf dir/                     # force recursive removal
python src/rm.py --                           # treat following args as files, not options
python src/rm.py --help                       # show help information
```

## `date` – Print or set the system date and time

```bash
python src/date.py                            # print current date/time (matches GNU date)
python src/date.py '+%Y-%m-%d %H:%M:%S'       # custom format
python src/date.py -d '2024-01-01 12:00:00'   # parse date string
python src/date.py -r file.txt                # show mtime of file.txt
python src/date.py -u                         # UTC output
python src/date.py -I                         # ISO 8601 output
python src/date.py --rfc-3339 seconds         # RFC 3339 output
python src/date.py -R                         # RFC 5322 (email) output
python src/date.py --help                     # show help information
```

## `pwd` – Print current directory

```bash
python src/pwd.py                             # print current directory (physical, default)
python src/pwd.py -L                          # logical mode (uses $PWD if valid)
python src/pwd.py -P                          # physical mode (resolves symlinks)
python src/pwd.py --help                      # show help information
```

## `touch` – Update file timestamps

```bash
python src/touch.py file.txt                  # create or update
python src/touch.py -d "2 hours ago" file     # set relative time
python src/touch.py -r ref.txt file           # copy timestamp
python src/touch.py -t 202501011200 file      # exact datetime
```

## `echo` – Display a line of text

```bash
python src/echo.py "Hello World"              # Hello World
python src/echo.py -n "No newline"            # No newline (no trailing newline)
python src/echo.py -e "Line 1\nLine 2"        # Line 1 followed by Line 2 on new line
python src/echo.py -e "Tab\there"             # Tab    here
python src/echo.py -e "Bell\a"                # Bell (might trigger a terminal beep)
python src/echo.py -e "Stop here\cIgnored"    # Stop here (output stops at \c)
python src/echo.py -e "\x41\x42\x43"          # ABC (hex codes)
python src/echo.py -e "\101\102\103"          # ABC (octal codes)
```

## `whoami` – Print current user name

```bash
python src/whoami.py                          # outputs current username
python src/whoami.py --help                   # show help information
python src/whoami.py --version                # show version information
```

## `nproc` – Print the number of processing units available

```bash
python src/nproc.py                           # number available to current process
python src/nproc.py --all                     # number of installed processors
python src/nproc.py --ignore=2                # exclude 2 processing units
python src/nproc.py --help                    # show help information
python src/nproc.py --version                 # show version information
```

## `sleep` – Pause for a specified amount of time

```bash
python src/sleep.py 5                         # sleep for 5 seconds
python src/sleep.py 2m                        # sleep for 2 minutes
python src/sleep.py 1h                        # sleep for 1 hour
python src/sleep.py 1.5d                      # sleep for 1.5 days
python src/sleep.py 1m 30s                    # sleep for 1 minute and 30 seconds (sum)
python src/sleep.py --help                    # show help information
python src/sleep.py --version                 # show version information
```

## `kill` – Send signals to processes, or list signals

```bash
python src/kill.py -l                       # list all signal names
python src/kill.py -l HUP 9                 # convert signal names/numbers
python src/kill.py -t                       # print a table of signals
python src/kill.py -9 1234                  # send SIGKILL to PID 1234
python src/kill.py -s HUP 5678              # send SIGHUP to PID 5678
python src/kill.py 4321                     # send SIGTERM (default) to PID 4321
python src/kill.py --help                   # show help information
python src/kill.py --version                # show version information
```

## `hostid` – print the hexadecimal identifier for the current host

```bash
python src/hostid.py                         # print the hexadecimal identifier
python src/hostid.py --help                  # show help information
python src/hostid.py --version               # show version information
```
