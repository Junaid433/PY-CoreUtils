# 🏗️ Project Architecture – PY-CoreUtils

## Overview

PY-CoreUtils is a modular, cross-platform Python port of GNU coreutils. Each utility is a standalone script in `src/`, designed for CLI use and easy extension. The project is organized for clarity, hackability, and testability.

---

## Directory Structure

```
PY-CoreUtils/
├── src/                # All main CLI utilities (one file per command)
├── tests/              # CLI and unit tests for each command
├── docs/               # Documentation (usage, features, architecture, ...)
├── .github/            # GitHub configs, issue/PR templates
├── CONTRIBUTING.md     # How to contribute
├── CODE_OF_CONDUCT.md  # Community guidelines
├── SECURITY.md         # Security policy
├── README.md           # Project overview
└── ...
```

---

## Design Principles

- **One file, one tool:** Each command (e.g., `rm`, `date`, `mkdir`) is a single Python script in `src/`.
- **CLI-first:** All logic is accessible from the command line, with `main()` as the entry point.
- **Separation of concerns:** CLI parsing is in `main()`, core logic is in helpers.
- **No dependencies:** Pure Python standard library for maximum portability.
- **Testable:** All commands have corresponding CLI tests in `tests/`.
- **Extensible:** New commands can be added by dropping a new script in `src/` and a test in `tests/`.

---

## Adding a New Command

1. **Create a new script:**
   - Place it in `src/yourcommand.py`.
   - Follow the style of existing commands (docstring, `main()`, helpers).
2. **Add tests:**
   - Create `tests/test_yourcommand_cli.py` for CLI tests.
   - Use `pytest` and subprocess for CLI testing.
3. **Document usage:**
   - Add examples to `docs/usage.md`.
   - Update the README table if desired.

---

## Example Command Structure

```python
#!/usr/bin/env python3
"""
mytool - short description
Python port of GNU coreutils mytool
"""
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(...)
    # Add arguments
    args = parser.parse_args()
    # CLI logic
    ...

if __name__ == '__main__':
    sys.exit(main())
```

---

## Testing Philosophy

- All CLI tools are tested via subprocess in `tests/`.
- Tests cover normal, edge, and error cases.
- No code is considered "done" without tests.

---

## Extending & Refactoring

- **Want to add a new GNU tool?**
  - Copy an existing script as a template.
  - Follow the CLI and logic separation pattern.
  - Add tests and usage docs.
- **Want to refactor?**
  - Keep CLI and core logic separate.
  - Ensure all tests pass before/after.

---

## Design Decisions

- **No external dependencies:** To maximize portability and ease of use.
- **Flat src/ structure:** Simple, discoverable, and easy to extend.
- **pytest for all tests:** Modern, powerful, and familiar to Python devs.
- **Docs in /docs:** Keeps the root clean and makes docs easy to find.

---

## Got Questions?

- See [CONTRIBUTING.md](../CONTRIBUTING.md) for how to get started.
- Open a [discussion](https://github.com/Junaid433/PY-CoreUtils/discussions) or [issue](https://github.com/Junaid433/PY-CoreUtils/issues) if you want to propose a change or ask about the architecture!
