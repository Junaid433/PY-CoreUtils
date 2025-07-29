import subprocess
import sys
import os
import tempfile
import time
from datetime import datetime

SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'touch.py'))

def run_cli(args):
    result = subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True)
    return result

def test_basic_touch():
    with tempfile.TemporaryDirectory() as tmpdir:
        f = os.path.join(tmpdir, 'file1.txt')
        result = run_cli([f])
        assert result.returncode == 0
        assert os.path.isfile(f)

def test_touch_no_create():
    with tempfile.TemporaryDirectory() as tmpdir:
        f = os.path.join(tmpdir, 'file2.txt')
        result = run_cli(['-c', f])
        assert result.returncode == 0
        assert not os.path.exists(f)

def test_touch_date():
    with tempfile.TemporaryDirectory() as tmpdir:
        f = os.path.join(tmpdir, 'file3.txt')
        t = int(datetime(2022, 1, 1, 12, 0, 0).timestamp())
        result = run_cli(['-d', '2022-01-01 12:00:00', f])
        assert result.returncode == 0
        assert os.path.isfile(f)
        stat = os.stat(f)
        assert abs(stat.st_mtime - t) < 2

def test_touch_posix_time():
    with tempfile.TemporaryDirectory() as tmpdir:
        f = os.path.join(tmpdir, 'file4.txt')
        result = run_cli(['-t', '202201011200', f])
        assert result.returncode == 0
        assert os.path.isfile(f)

def test_touch_help():
    result = run_cli(['--help'])
    assert 'Usage:' in result.stdout
    assert result.returncode == 0

def test_touch_version():
    result = run_cli(['--version'])
    assert 'touch (Python port of GNU coreutils)' in result.stdout
    assert result.returncode == 0

def test_touch_missing_operand():
    result = run_cli([])
    assert 'missing file operand' in result.stderr
    assert result.returncode == 1

def test_touch_invalid_date():
    with tempfile.TemporaryDirectory() as tmpdir:
        f = os.path.join(tmpdir, 'file5.txt')
        result = run_cli(['-d', 'bad-date', f])
        assert 'invalid date format' in result.stderr
        assert result.returncode == 1
