# 🐍 Python Coreutils – GNU Coreutils Rewritten in Pure Python

> A cross-platform, pure Python implementation of essential [GNU Coreutils](https://www.gnu.org/software/coreutils/). This project offers a drop-in alternative for developers seeking CLI tools compatible with Windows, macOS, and Linux.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)
[![CI](https://github.com/Junaid433/PYCoreUtils/actions/workflows/python-tests.yml/badge.svg)](https://github.com/Junaid433/PYCoreUtils/actions)

---

## 📦 Overview

This project ports essential [GNU Coreutils](https://www.gnu.org/software/coreutils/) commands to **pure Python**, enabling seamless use of familiar Unix command-line utilities on **any platform**. Each command aims to match the original GNU behavior, argument structure, and output format.

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
| `pwd`      | ✅ DONE |
| `chmod`    | ⏳ TODO |

---

## 📖 Documentation

- [Usage Examples](docs/usage.md)
- [Features](docs/features.md)

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
python pwd.py --help
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

`gnu coreutils` `python coreutils` `unix utilities` `cross-platform cli` `command-line tools` `mkdir in python` `basename` `touch` `chmod` `rm` `date` `pwd` `pure python` `no dependencies` `drop-in replacement` `coreutils alternative` `cli tools`
