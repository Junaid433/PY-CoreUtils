import pytest
import sys
import os
from io import StringIO
from echo import process_escapes, hextobin
import subprocess

def test_hextobin():
    assert hextobin('0') == 0
    assert hextobin('9') == 9
    assert hextobin('a') == 10
    assert hextobin('A') == 10
    assert hextobin('f') == 15
    assert hextobin('F') == 15

def test_process_escapes_basic():
    s, cont = process_escapes('foo')
    assert s == 'foo' and cont
    s, cont = process_escapes('foo\\nbar')
    assert s == 'foo\nbar' and cont
    s, cont = process_escapes('foo\\tbar')
    assert s == 'foo\tbar' and cont
    s, cont = process_escapes('foo\\cbar')
    assert s == 'foo' and not cont
    s, cont = process_escapes('foo\\x41')
    assert s == 'fooA' and cont
    s, cont = process_escapes('foo\\041')
    assert s == 'foo!' and cont
    s, cont = process_escapes('foo\\e')
    assert s == 'foo\x1b' and cont
    s, cont = process_escapes('foo\\\\bar')
    assert s == 'foo\\bar' and cont

def run_cli(args):
    cmd = [sys.executable, os.path.abspath('echo.py')] + args
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result

def test_cli_basic():
    result = run_cli(['hello', 'world'])
    assert result.stdout == 'hello world\n'
    assert result.returncode == 0

def test_cli_n():
    result = run_cli(['-n', 'hello'])
    assert result.stdout == 'hello'
    assert result.returncode == 0

def test_cli_e():
    result = run_cli(['-e', 'foo\\nbar'])
    assert result.stdout == 'foo\nbar\n'
    assert result.returncode == 0

def test_cli_E():
    result = run_cli(['-E', 'foo\\nbar'])
    assert result.stdout == 'foo\\nbar\n'
    assert result.returncode == 0

def test_cli_escape_sequences():
    result = run_cli(['-e', 'A\\tB\\nC'])
    assert result.stdout == 'A\tB\nC\n'.replace('\\t', '\t').replace('\\n', '\n')
    assert result.returncode == 0

def test_cli_c_ends_output():
    result = run_cli(['-e', 'foo\\cbar'])
    assert result.stdout == 'foo'
    assert result.returncode == 0

def test_cli_help():
    result = run_cli(['--help'])
    assert 'Usage:' in result.stdout
    assert result.returncode == 0

def test_cli_version():
    result = run_cli(['--version'])
    assert 'echo (Python port of GNU coreutils)' in result.stdout
    assert result.returncode == 0
