<div align="center">

# 🐍 PYCoreUtils

**The Modern, Cross-Platform Python Port of GNU Coreutils**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)
[![CI](https://github.com/Junaid433/PYCoreUtils/actions/workflows/python-tests.yml/badge.svg)](https://github.com/Junaid433/PYCoreUtils/actions)

</div>

---

> **✨ Unix CLI power, Pythonic flexibility. Run coreutils anywhere.**

---

## 🚀 Why PYCoreUtils?

- 🖥️ **Cross-platform**: Linux, macOS, Windows — no C toolchain needed.
- 🧩 **Drop-in CLI tools**: Familiar commands, same flags, same output.
- 🐍 **Pure Python**: No dependencies, hackable, readable, and extendable.
- 💡 **Great for scripting, teaching, and dev environments**.
- 🔥 **Modern code, modern vibes.**

---

## 🛠️ Quick Start

```bash
git clone https://github.com/Junaid433/PYCoreUtils.git
cd PYCoreUtils
python mkdir.py --help
python rm.py --help
python date.py --help
```

---

## 🧑‍💻 Coreutils, Python Style

| Command      | Status |  | Command    | Status |
| ------------ | ------ |--| ---------- | ------ |
| `basename`   | ✅     |  | `date`     | ✅     |
| `mkdir`      | ✅     |  | `echo`     | ✅     |
| `touch`      | ✅     |  | `whoami`   | ✅     |
| `rm`         | ✅     |  | `pwd`      | ✅     |
| `ls`         | ⏳     |  | `cp`       | ⏳     |
| `mv`         | ⏳     |  | `cat`      | ⏳     |
| `head`       | ⏳     |  | `tail`     | ⏳     |
| `chmod`      | ⏳     |  |            |        |

---

## 🌈 CLI Showcase

```bash
$ python rm.py -rf build/
$ python date.py '+%Y-%m-%d %H:%M:%S'
$ python mkdir.py -p src/utils
$ python pwd.py
$ python basename.py /usr/bin/python3
$ python echo.py -e "Hello\nWorld!"
```

---

## 📚 [Full Usage & Features →](docs/usage.md)

- [Usage Examples](docs/usage.md)
- [Features](docs/features.md)

---

## ✨ Features at a Glance

- **Full GNU-style CLI**: All major flags, help/version, error codes.
- **Logical/Physical path handling**: `pwd` supports -L/-P, symlinks, POSIXLY_CORRECT.
- **Date/time power**: `date` supports parsing, formatting, reference file, UTC, batch, and more.
- **Safe & robust**: `rm` has interactive, force, and recursive modes.
- **No C, no build, no nonsense**: Just Python.

---

## 🧪 Testing & Quality

- 100% pytest coverage for all commands
- [GitHub Actions](https://github.com/Junaid433/PYCoreUtils/actions) CI
- Follows [PEP 8](https://peps.python.org/pep-0008/)

---

## 🤝 Community & Contributing

- Star ⭐ the repo if you like it!
- PRs, issues, and feedback welcome.
- See [CONTRIBUTING.md](CONTRIBUTING.md) (coming soon)

---

## 📄 License

[GNU GPL v3 or later](https://www.gnu.org/licenses/gpl-3.0.html)

---

<div align="center">

💡 **Hack, learn, and build with Python-powered coreutils!**

</div>
