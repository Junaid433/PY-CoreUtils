<div align="center">

# 🐍✨ PYCoreUtils

**The Modern, Cross-Platform Python Port of GNU Coreutils**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)
[![CI](https://github.com/Junaid433/PYCoreUtils/actions/workflows/python-tests.yml/badge.svg)](https://github.com/Junaid433/PYCoreUtils/actions)
[![Open Issues](https://img.shields.io/github/issues/Junaid433/PYCoreUtils?color=orange)](https://github.com/Junaid433/PYCoreUtils/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

</div>

---

> **✨ Unix CLI power, Pythonic flexibility. Run coreutils anywhere.**

---

## 🌟 Why PYCoreUtils?

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

<details>
<summary><b>🌈 CLI Demos (click to expand)</b></summary>

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

## ✨ What Makes This Cool?

- **Full GNU-style CLI**: All major flags, help/version, error codes.
- **Logical/Physical path handling**: `pwd` supports -L/-P, symlinks, POSIXLY_CORRECT.
- **Date/time power**: `date` supports parsing, formatting, reference file, UTC, batch, and more.
- **Safe & robust**: `rm` has interactive, force, and recursive modes.
- **No C, no build, no nonsense**: Just Python.
- **100% pytest coverage** and [GitHub Actions](https://github.com/Junaid433/PYCoreUtils/actions) CI.

---

## 📚 [Full Usage, Features & Architecture →](docs/usage.md)

- [Usage Examples](docs/usage.md)
- [Features](docs/features.md)
- [Project Architecture](docs/architecture.md)

---

## 🗺️ Roadmap & Vision

- [ ] More GNU tools: `ls`, `cp`, `mv`, `cat`, `head`, `tail`, `chmod`, ...
- [ ] Windows/macOS-specific improvements
- [ ] More docs, more examples, more tests
- [ ] Community-driven features (your ideas here!)

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

## 💡 Did you know?

> You can use PYCoreUtils as a teaching tool, a scripting Swiss Army knife, or even as a base for your own Python CLI projects. Fork it, hack it, and make it yours!

---

## 📄 License

[GNU GPL v3 or later](https://www.gnu.org/licenses/gpl-3.0.html)

---

<div align="center">

💡 <b>Hack, learn, and build with Python-powered coreutils!</b>

</div>
