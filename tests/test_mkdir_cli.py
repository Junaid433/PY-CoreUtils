import subprocess
import sys
import os
import tempfile
import shutil

SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'mkdir.py'))

def run_cli(args):
    result = subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True)
    return result

def test_basic_mkdir():
    with tempfile.TemporaryDirectory() as tmpdir:
        d = os.path.join(tmpdir, 'newdir')
        result = run_cli([d])
        assert result.returncode == 0
        assert os.path.isdir(d)

def test_mkdir_parents():
    with tempfile.TemporaryDirectory() as tmpdir:
        d = os.path.join(tmpdir, 'a/b/c/d')
        result = run_cli(['-p', d])
        assert result.returncode == 0
        assert os.path.isdir(d)

def test_mkdir_verbose():
    with tempfile.TemporaryDirectory() as tmpdir:
        d = os.path.join(tmpdir, 'vdir')
        result = run_cli(['-v', d])
        assert result.returncode == 0
        assert 'created directory' in result.stdout
        assert os.path.isdir(d)

def test_mkdir_mode():
    with tempfile.TemporaryDirectory() as tmpdir:
        d = os.path.join(tmpdir, 'modedir')
        result = run_cli(['-m', '700', d])
        assert result.returncode == 0
        assert os.path.isdir(d)
        mode = oct(os.stat(d).st_mode & 0o777)
        assert mode == '0o700'

def test_mkdir_help():
    result = run_cli(['--help'])
    assert 'Usage:' in result.stdout
    assert result.returncode == 0

def test_mkdir_version():
    result = run_cli(['--version'])
    assert 'mkdir (Python port of GNU coreutils)' in result.stdout
    assert result.returncode == 0

def test_mkdir_missing_operand():
    result = run_cli([])
    assert 'missing operand' in result.stderr
    assert result.returncode == 1

def test_mkdir_invalid_mode():
    with tempfile.TemporaryDirectory() as tmpdir:
        d = os.path.join(tmpdir, 'badmodedir')
        result = run_cli(['-m', 'badmode', d])
        assert 'invalid mode' in result.stderr
        assert result.returncode == 1
