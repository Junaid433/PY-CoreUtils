import subprocess
import sys
import os
import tempfile

SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'nproc.py'))

def run_cli(args, input_text=None):
    return subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True, input=input_text)

def test_basic_nproc():
    result = run_cli([])
    assert result.returncode == 0
    assert result.stdout.strip().isdigit()
    assert int(result.stdout.strip()) >= 1

def test_all_option():
    result = run_cli(['--all'])
    assert result.returncode == 0
    assert result.stdout.strip().isdigit()
    assert int(result.stdout.strip()) >= 1

def test_ignore_option():
    result = run_cli(['--ignore=1'])
    assert result.returncode == 0
    assert result.stdout.strip().isdigit()
    assert int(result.stdout.strip()) >= 1

def test_ignore_option_too_large():
    # Use a large ignore value to force clamp to 1
    result = run_cli(['--ignore=9999'])
    assert result.returncode == 0
    assert result.stdout.strip() == '1'

def test_ignore_missing_argument():
    result = run_cli(['--ignore'])
    assert result.returncode == 1
    assert 'requires an argument' in result.stderr

def test_ignore_invalid_argument():
    result = run_cli(['--ignore=foo'])
    assert result.returncode == 1
    assert 'invalid number' in result.stderr

def test_extra_operand():
    result = run_cli(['foo'])
    assert result.returncode == 1
    assert 'extra operand' in result.stderr

def test_help():
    result = run_cli(['--help'])
    assert 'Usage:' in result.stdout or 'usage:' in result.stdout.lower()
    assert result.returncode == 0

def test_version():
    result = run_cli(['--version'])
    assert 'nproc (Python port of GNU coreutils)' in result.stdout
    assert result.returncode == 0

def test_unrecognized_option():
    result = run_cli(['--notanoption'])
    assert result.returncode == 1
    assert 'unrecognized option' in result.stderr
