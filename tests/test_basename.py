import pytest
import sys
import os
from io import StringIO
from basename import (
    remove_suffix, strip_trailing_slashes, is_absolute_path,
    get_file_system_prefix_len, base_name, perform_basename
)

# --- Unit tests for core logic functions ---
def test_remove_suffix():
    assert remove_suffix('file.txt', '.txt') == 'file'
    assert remove_suffix('file.txt', '.md') == 'file.txt'
    assert remove_suffix('file.txt', '') == 'file.txt'
    assert remove_suffix('file', 'file') == 'file'
    assert remove_suffix('filefile', 'file') == 'file'
    assert remove_suffix('file', 'longsuffix') == 'file'

def test_strip_trailing_slashes():
    assert strip_trailing_slashes('foo/bar/') == 'foo/bar'
    assert strip_trailing_slashes('foo/bar////') == 'foo/bar'
    assert strip_trailing_slashes('/') == '/'
    assert strip_trailing_slashes('C:\\') == 'C:\\'
    assert strip_trailing_slashes('C:/foo/') == 'C:/foo'

def test_is_absolute_path():
    assert is_absolute_path('/foo/bar')
    assert is_absolute_path('C:/foo')
    assert is_absolute_path('C:')
    assert not is_absolute_path('foo/bar')

def test_get_file_system_prefix_len():
    assert get_file_system_prefix_len('C:') == 2
    assert get_file_system_prefix_len('C:/foo') == 2
    assert get_file_system_prefix_len('/foo') == 0
    assert get_file_system_prefix_len('foo') == 0

def test_base_name():
    assert base_name('/usr/bin/sort') == 'sort'
    assert base_name('include/stdio.h') == 'stdio.h'
    assert base_name('/') == '/'
    assert base_name('//') == '//'
    assert base_name('C:') == 'C:'
    assert base_name('foo/bar/') == 'bar'
    assert base_name('') == '.'

# --- Integration test for perform_basename (output capture) ---
def test_perform_basename_stdout(monkeypatch):
    out = StringIO()
    monkeypatch.setattr(sys, 'stdout', out)
    perform_basename('/usr/bin/sort', None, False)
    assert out.getvalue().strip() == 'sort'
    out = StringIO()
    monkeypatch.setattr(sys, 'stdout', out)
    perform_basename('include/stdio.h', '.h', False)
    assert out.getvalue().strip() == 'stdio'
    out = StringIO()
    monkeypatch.setattr(sys, 'stdout', out)
    perform_basename('foo.txt', '.md', False)
    assert out.getvalue().strip() == 'foo.txt'
    out = StringIO()
    monkeypatch.setattr(sys, 'stdout', out)
    perform_basename('foo.txt', None, True)
    assert out.getvalue() == 'foo.txt\0'

# --- CLI tests using subprocess ---
import subprocess
import sys

def run_cli(args):
    cmd = [sys.executable, os.path.abspath('basename.py')] + args
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result

def test_cli_basic():
    result = run_cli(['/usr/bin/sort'])
    assert result.stdout.strip() == 'sort'
    assert result.returncode == 0

def test_cli_suffix():
    result = run_cli(['include/stdio.h', '.h'])
    assert result.stdout.strip() == 'stdio'
    assert result.returncode == 0

def test_cli_multiple():
    result = run_cli(['-a', 'foo/bar', 'baz/qux'])
    lines = result.stdout.strip().split('\n')
    assert lines == ['bar', 'qux']
    assert result.returncode == 0

def test_cli_zero():
    result = run_cli(['-z', '/usr/bin/sort'])
    assert result.stdout == 'sort\0'
    assert result.returncode == 0

def test_cli_help():
    result = run_cli(['--help'])
    assert 'Usage:' in result.stdout
    assert result.returncode == 0

def test_cli_version():
    result = run_cli(['--version'])
    assert 'basename (Python port of GNU coreutils)' in result.stdout
    assert result.returncode == 0

def test_cli_missing_operand():
    result = run_cli([])
    assert 'missing operand' in result.stderr
    assert result.returncode == 1

def test_cli_extra_operand():
    result = run_cli(['foo', 'bar', 'baz'])
    assert 'extra operand' in result.stderr
    assert result.returncode == 1
