# 🐍 Python Coreutils – GNU Coreutils Rewritten in Pure Python

> A cross-platform, pure Python implementation of essential [GNU Coreutils](https://www.gnu.org/software/coreutils/). This project offers a drop-in alternative for developers seeking CLI tools compatible with Windows, macOS, and Linux.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)

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
| `rm`       | ⏳ TODO |
| `cp`       | ⏳ TODO |
| `mv`       | ⏳ TODO |
| `cat`      | ⏳ TODO |
| `head`     | ⏳ TODO |
| `tail`     | ⏳ TODO |
| `date`     | ⏳ TODO |
| `echo`     | ✅ DONE |
| `whoami`   | ⏳ TODO |
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

---

## 🧠 Implementation Highlights

* ✅ Robust argument parsing (no external libraries)
* ✅ Accurate GNU-style error handling and formatting
* ✅ Efficient file and directory operations
* ✅ Platform-specific abstraction for consistent behavior

---

## 📋 Technical Details

### Requirements

* Python **3.6+**
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
git clone https://github.com/yourusername/python-coreutils.git
cd python-coreutils

python mkdir.py --help
python touch.py --help
python basename.py --help
```

Or run individual scripts as needed.

---

## 🧪 Development & Testing

* 🧹 Follows [PEP 8](https://peps.python.org/pep-0008/)
* 📘 Inline docstrings and typing hints
* 🧪 Manual testing across:

  * GNU output diffing
  * Edge cases and invalid input
  * Platform variations (Windows/macOS/Linux)

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

`gnu coreutils` `python coreutils` `unix utilities` `cross-platform cli` `command-line tools` `mkdir in python` `basename` `touch` `chmod` `pure python` `no dependencies` `drop-in replacement` `coreutils alternative` `cli tools`