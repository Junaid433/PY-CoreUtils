# 🐍 Python Coreutils – GNU Coreutils Rewritten in Pure Python

> A cross-platform, pure Python implementation of essential [GNU Coreutils](https://www.gnu.org/software/coreutils/). This project offers a drop-in alternative for developers seeking CLI tools compatible with Windows, macOS, and Linux.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)
[![CI](https://github.com/Junaid433/PYCoreUtils/actions/workflows/python-tests.yml/badge.svg)](https://github.com/Junaid433/PYCoreUtils/actions)

---

## 📦 Overview

This project ports essential [GNU Coreutils](https://www.gnu.org/software/coreutils/) commands to **pure Python**, enabling seamless use of familiar Unix command-line utilities on **any platform**. Each command aims to match the original GNU behavior, argument structure, and output format.

It’s perfect for:

* Python developers who want native CLI tools
* Cross-platform scripting without dependencies
* Windows users needing Unix-like commands

---

## ✅ Implemented Commands

| Command    | Status |
| ---------- | ------ |
| `basename` | ✅ DONE |
| `mkdir`    | ✅ DONE |
| `touch`    | ✅ DONE |
| `ls`       | ⏳ TODO |
| `rm`       | ✅ DONE |
| `cp`       | ⏳ TODO |
| `mv`       | ⏳ TODO |
| `cat`      | ⏳ TODO |
| `head`     | ⏳ TODO |
| `tail`     | ⏳ TODO |
| `date`     | ✅ DONE |
| `echo`     | ✅ DONE |
| `whoami`   | ✅ DONE |
| `pwd`      | ⏳ TODO |
| `chmod`    | ⏳ TODO |

---

## 🚀 Features

### 🧩 Full Command-Line Compatibility

* Same options and flags as GNU Coreutils (`-h`, `--help`, `--version`)
* Matching error messages and exit codes
* Identical usage output and syntax

### 💻 Cross-Platform Support

* Compatible with **Windows**, **macOS**, and **Linux**
* Handles platform-specific file paths and permissions
* Symbolic link and timestamp support where available

### 🔧 Advanced Functionality

* `mkdir`: Full symbolic mode parsing (`u=rwx,g=rx,o=r`)
* `touch`: Legacy POSIX timestamp formats + relative dates
* `basename`: Multiple file support and suffix stripping
* `rm`: Full GNU-style recursive, interactive, and safe deletion
* `date`: GNU-style formatting, parsing, reference file, UTC, batch, and locale support

---

## 🛠 Usage Examples

### `basename` – Extract filename from path

```bash
python basename.py /usr/bin/sort          # outputs: sort
python basename.py include/stdio.h .h     # outputs: stdio
python basename.py -a file1.txt file2.c   # outputs: file1 file2
```

### `mkdir` – Create directories

```bash
python mkdir.py newdir                    # simple directory
python mkdir.py -p a/b/c/d                # nested structure
python mkdir.py -m 755 newdir             # numeric permissions
python mkdir.py -m u=rwx,g=rx,o=r newdir  # symbolic permissions
```

### `rm` – Remove files and directories

```bash
python rm.py file.txt                     # remove a file
python rm.py -f missing.txt               # ignore missing files
python rm.py -i file.txt                  # prompt before removal
python rm.py -r dir/                      # recursively remove directory
python rm.py -rf dir/                     # force recursive removal
python rm.py --                           # treat following args as files, not options
python rm.py --help                       # show help information
```

### `date` – Print or set the system date and time

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

### `touch` – Update file timestamps

```bash
python touch.py file.txt                  # create or update
python touch.py -d "2 hours ago" file     # set relative time
python touch.py -r ref.txt file           # copy timestamp
python touch.py -t 202501011200 file      # exact datetime
```

### `echo` – Display a line of text

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

### `whoami` – Print current user name

```bash
python whoami.py                          # outputs current username
python whoami.py --help                   # show help information
python whoami.py --version                # show version information
```
---

## 🧠 Implementation Highlights

* ✅ Robust argument parsing (no external libraries)
* ✅ Accurate GNU-style error handling and formatting
* ✅ Efficient file and directory operations
* ✅ Platform-specific abstraction for consistent behavior

---

## 📋 Technical Details

### Requirements

* Python **3.6+** (tested up to 3.13)
* No third-party libraries (pure `stdlib`)

### Architecture

* Modular and reusable codebase
* Unified error handling and CLI interface
* POSIX-inspired, but adapted for Python and cross-platform needs

### Compatibility Notes

| Feature          | Notes                                    |
| ---------------- | ---------------------------------------- |
| File Permissions | Full on Unix, partial on Windows         |
| Timestamps       | Nanosecond precision where supported     |
| Symbolic Links   | Supported on Unix, limited on Windows    |
| SELinux/SMACK    | Not implemented, placeholder stubs exist |

---

## 📦 Installation

No setup required. Just clone and run:

```bash
git clone https://github.com/Junaid433/PYCoreUtils.git
cd PYCoreUtils

python mkdir.py --help
python touch.py --help
python basename.py --help
python rm.py --help
python date.py --help
```

Or run individual scripts as needed.

---

## 🧪 Development & Testing

* 🧹 Follows [PEP 8](https://peps.python.org/pep-0008/)
* 📘 Inline docstrings and typing hints
* 🧪 Manual and automated testing:
  * Automated: [pytest](https://docs.pytest.org/) (see below)
  * Manual: GNU output diffing, edge cases, platform variations

### Running Tests

To run all tests locally:

```bash
pip install pytest
pytest
```

Tests are also run automatically on every push and pull request via [GitHub Actions](https://github.com/Junaid433/PYCoreUtils/actions).

---

## 🤝 Contributing

Contributions are welcome! Please open issues or pull requests for bug fixes, new features, or improvements. Make sure to add or update tests for any code changes.

---

## 📚 Related Projects

* [GNU Coreutils (C)](https://www.gnu.org/software/coreutils/)
* [BusyBox](https://busybox.net/)
* [uutils/coreutils (Rust)](https://github.com/uutils/coreutils)

---

## 📄 License

Licensed under the [GNU GPL v3 or later](https://www.gnu.org/licenses/gpl-3.0.html). Compatible with the original Coreutils licensing.

---

## 🔍 Keywords

`gnu coreutils` `python coreutils` `unix utilities` `cross-platform cli` `command-line tools` `mkdir in python` `basename` `touch` `chmod` `rm` `date` `pure python` `no dependencies` `drop-in replacement` `coreutils alternative` `cli tools`
