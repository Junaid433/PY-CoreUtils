# Features

## Full Command-Line Compatibility

* Same options and flags as GNU Coreutils (`-h`, `--help`, `--version`)
* Matching error messages and exit codes
* Identical usage output and syntax

## Cross-Platform Support

* Compatible with **Windows**, **macOS**, and **Linux**
* Handles platform-specific file paths and permissions
* Symbolic link and timestamp support where available

## Utility Features

### `basename`
* Extracts filename from a given path.
* Supports multiple files and optional suffix stripping.
* Matches GNU basename behavior and output.

### `date`
* Prints or sets the system date and time.
* Supports custom formatting, parsing, UTC, ISO, RFC, and locale output.
* Can show file modification times and parse date strings.
* Matches GNU date options and output.

### `echo`
* Displays a line of text to standard output.
* Supports escape sequences (e.g., `\n`, `\t`, `\a`, `\c`, hex, octal).
* `-n` suppresses trailing newline, `-e` enables interpretation of escapes.
* Matches GNU echo behavior.

### `mkdir`
* Creates directories, including nested structures with `-p`.
* Supports numeric and symbolic permission modes.
* Handles existing directories gracefully.
* Matches GNU mkdir options and output.

### `nproc`
* Prints the number of processing units available to the current process.
* Supports `--all` and `--ignore=N` options.
* Matches GNU nproc behavior and output.

### `pwd`
* Prints the current working directory.
* Supports logical (`-L`) and physical (`-P`) modes.
* Handles symlinks and POSIXLY_CORRECT.
* Matches GNU pwd options and output.

### `rm`
* Removes files and directories.
* Supports recursive (`-r`), force (`-f`), and interactive (`-i`) modes.
* Handles missing files, directories, and safe deletion.
* Matches GNU rm options and output.

### `sleep`
* Pauses execution for a specified amount of time.
* Accepts multiple time intervals (e.g., `1m 30s`), summing them.
* Supports suffixes: `s` (seconds), `m` (minutes), `h` (hours), `d` (days).
* Provides help/version output and matches GNU sleep behavior.

### `touch`
* Updates file timestamps or creates files if they do not exist.
* Supports legacy POSIX timestamp formats, relative dates, and reference files.
* Can set exact datetimes and copy timestamps from other files.
* Matches GNU touch options and output.

### `whoami`
* Prints the current user's username.
* Supports `--help` and `--version` options.
* Matches GNU whoami behavior and output.

### `kill`
* Sends signals to processes or process groups by PID.
* Accepts signal by name (e.g., HUP, KILL) or number (e.g., 1, 9), with or without SIG prefix.
* Supports `-s SIGNAL`, `-SIGNAL`, and default SIGTERM.
* Lists signals (`-l`), converts names/numbers, and prints a table (`-t`).
* Provides help/version output and matches GNU kill behavior.
* Returns nonzero exit code for invalid signals, PIDs, or errors.

### `hostid`
* Prints the hexadecimal identifier for the current host.
* Matches GNU hostid behavior and output.

### `hostname`
* Prints the current system's hostname.
* Can set the system's hostname (if run with sufficient privileges).
* Matches GNU hostname behavior and output.

### `id`
* Prints real and effective user and group IDs, or all groups for a user.
* Supports `-u` (user), `-g` (group), `-G` (groups), `-n` (name), `-r` (real), `-z` (NUL delimiter), and more.
* Resolves names or prints numeric IDs, matching GNU id output and error handling.
* Can print info for the current user or a specified user/UID.
* Provides help/version output and matches GNU id behavior and output.

### `users`
*Prints the login names of users currently logged in.
* Supports specifying an alternative `utmp` or `wtmp` file.
* Matches GNU users behavior and output.