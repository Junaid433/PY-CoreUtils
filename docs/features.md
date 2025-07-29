# Features

## Full Command-Line Compatibility

* Same options and flags as GNU Coreutils (`-h`, `--help`, `--version`)
* Matching error messages and exit codes
* Identical usage output and syntax

## Cross-Platform Support

* Compatible with **Windows**, **macOS**, and **Linux**
* Handles platform-specific file paths and permissions
* Symbolic link and timestamp support where available

## Advanced Functionality

* `mkdir`: Full symbolic mode parsing (`u=rwx,g=rx,o=r`)
* `touch`: Legacy POSIX timestamp formats + relative dates
* `basename`: Multiple file support and suffix stripping
* `rm`: Full GNU-style recursive, interactive, and safe deletion
* `date`: GNU-style formatting, parsing, reference file, UTC, batch, and locale support
* `pwd`: Logical/physical mode, POSIXLY_CORRECT, symlink handling
