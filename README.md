<div align="center">

<img src="https://raw.githubusercontent.com/Junaid433/PYCoreUtils/main/docs/banner.png" alt="PYCoreUtils Banner" width="600"/>

# 🐍 PYCoreUtils

**The Modern, Cross-Platform Python Port of GNU Coreutils**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)
[![CI](https://github.com/Junaid433/PYCoreUtils/actions/workflows/python-tests.yml/badge.svg)](https://github.com/Junaid433/PYCoreUtils/actions)

</div>

---

> <img src="https://img.shields.io/badge/Unix%20CLI%20Power-Pythonic%20Flexibility-blueviolet?style=flat-square"/>  
> <b>✨ Run coreutils anywhere. Hackable, readable, and fun.</b>

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
# Clone and run any tool instantly!
git clone https://github.com/Junaid433/PYCoreUtils.git
cd PYCoreUtils
python src/mkdir.py --help
python src/rm.py --help
python src/date.py --help
```

---

## 🧑‍💻 Coreutils, Python Style

| Command      | Status |  | Command    | Status |
| ------------ | ------ |--| ---------- | ------ |
| `basename`   | ✅     |  | `date`     | ✅     |
| `mkdir`      | ✅     |  | `echo`     | ✅     |
| `touch`      | ✅     |  | `whoami`   | ✅     |
| `rm`         | ✅     |  | `pwd`      | ✅     |
| `unlink`     | ⏳     |  | `link`     | ⏳     |
| `uptime`     | ⏳     |  | `groups`   | ⏳     |
| `users`      | ⏳     |  | `ls`       | ⏳     |
| `kill`       | ⏳     |  |            |        |

---

## 🌈 Screenshots & Demo

> <b>Real CLI output, real Python code.</b>

<p align="center">
  <img src="https://raw.githubusercontent.com/Junaid433/PYCoreUtils/main/docs/demo_rm.png" alt="rm demo" width="500"/>
  <img src="https://raw.githubusercontent.com/Junaid433/PYCoreUtils/main/docs/demo_date.png" alt="date demo" width="500"/>
</p>

<details>
<summary>Show CLI Examples</summary>

```bash
$ python src/rm.py -rf build/
$ python src/date.py '+%Y-%m-%d %H:%M:%S'
$ python src/mkdir.py -p src/utils
$ python src/pwd.py
$ python src/basename.py /usr/bin/python3
$ python src/echo.py -e "Hello\nWorld!"
```
</details>

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

## 💬 Get Involved!

> **We welcome all contributors—new and experienced!**
>
> - [Contributing Guide](CONTRIBUTING.md)
> - [Code of Conduct](CODE_OF_CONDUCT.md)
> - [Security Policy](SECURITY.md)
> - [Open Issues](https://github.com/Junaid433/PYCoreUtils/issues)
> - [Discussions](https://github.com/Junaid433/PYCoreUtils/discussions)

Star ⭐ the repo, share it, and help us build the best Python-powered coreutils!

---

## 📄 License

[GNU GPL v3 or later](https://www.gnu.org/licenses/gpl-3.0.html)

---

<div align="center">

<img src="https://raw.githubusercontent.com/Junaid433/PYCoreUtils/main/docs/vibe_footer.png" alt="PYCoreUtils Vibes" width="400"/>

💡 <b>Hack, learn, and build with Python-powered coreutils!</b>

</div>
