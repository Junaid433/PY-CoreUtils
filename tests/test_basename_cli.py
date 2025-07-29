import subprocess
import sys
import os

SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'basename.py'))


def run_cli(args):
    result = subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True)
    return result


def test_basic_usage():
    result = run_cli(['/usr/bin/sort'])
    assert result.stdout.strip() == 'sort'
    assert result.returncode == 0


def test_suffix_removal():
    result = run_cli(['include/stdio.h', '.h'])
    assert result.stdout.strip() == 'stdio'
    assert result.returncode == 0


def test_suffix_flag():
    result = run_cli(['-s', '.h', 'include/stdio.h'])
    assert result.stdout.strip() == 'stdio'
    assert result.returncode == 0


def test_multiple_names():
    result = run_cli(['-a', 'any/str1', 'any/str2'])
    lines = result.stdout.strip().split('\n')
    assert lines == ['str1', 'str2']
    assert result.returncode == 0


def test_zero_terminated():
    result = run_cli(['-z', '/usr/bin/sort'])
    assert result.stdout.endswith('\0')
    assert 'sort' in result.stdout
    assert result.returncode == 0


def test_missing_operand():
    result = run_cli([])
    assert 'missing operand' in result.stderr
    assert result.returncode == 1


def test_extra_operand():
    result = run_cli(['a', 'b', 'c'])
    assert 'extra operand' in result.stderr
    assert result.returncode == 1


def test_help():
    result = run_cli(['--help'])
    assert 'Usage:' in result.stdout
    assert result.returncode == 0


def test_version():
    result = run_cli(['--version'])
    assert 'basename (Python port of GNU coreutils)' in result.stdout
    assert result.returncode == 0
