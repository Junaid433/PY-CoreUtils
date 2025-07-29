import subprocess
import sys
import os
import tempfile
import shutil

SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'rm.py'))

def run_cli(args, input_text=None):
    return subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True, input=input_text)

def test_basic_remove():
    with tempfile.TemporaryDirectory() as tmpdir:
        f = os.path.join(tmpdir, 'afile.txt')
        with open(f, 'w'):
            pass
        result = run_cli([f])
        assert result.returncode == 0
        assert not os.path.exists(f)

def test_force_missing():
    with tempfile.TemporaryDirectory() as tmpdir:
        f = os.path.join(tmpdir, 'nofile.txt')
        result = run_cli(['-f', f])
        assert result.returncode == 0
        assert not os.path.exists(f)

def test_remove_directory_recursive():
    with tempfile.TemporaryDirectory() as tmpdir:
        d = os.path.join(tmpdir, 'adir')
        os.mkdir(d)
        f = os.path.join(d, 'file.txt')
        with open(f, 'w'):
            pass
        result = run_cli(['-r', d])
        assert result.returncode == 0
        assert not os.path.exists(d)

def test_remove_directory_no_recursive():
    with tempfile.TemporaryDirectory() as tmpdir:
        d = os.path.join(tmpdir, 'adir')
        os.mkdir(d)
        result = run_cli([d])
        assert result.returncode == 1
        assert os.path.exists(d)

def test_interactive_remove_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        f = os.path.join(tmpdir, 'afile.txt')
        with open(f, 'w'):
            pass
        result = run_cli(['-i', f], input_text='y\n')
        assert result.returncode == 0
        assert not os.path.exists(f)

def test_interactive_remove_file_decline():
    with tempfile.TemporaryDirectory() as tmpdir:
        f = os.path.join(tmpdir, 'afile.txt')
        with open(f, 'w'):
            pass
        result = run_cli(['-i', f], input_text='n\n')
        assert result.returncode == 0
        assert os.path.exists(f)

def test_help():
    result = run_cli(['--help'])
    assert 'Usage:' in result.stdout or 'usage:' in result.stdout.lower()
    assert result.returncode == 0

def test_version():
    result = run_cli(['--version'])
    assert 'rm (Python port of GNU coreutils)' in result.stdout
    assert result.returncode == 0

def test_missing_operand():
    result = run_cli([])
    assert 'missing operand' in result.stderr
    assert result.returncode == 1
