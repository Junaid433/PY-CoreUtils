import pytest
import os
import sys
import tempfile
import shutil
import time
from touch import parse_posix_time, parse_date_string, touch_file
import subprocess
from datetime import datetime

def test_parse_posix_time():
    now = datetime.now()
    # MMDDhhmm
    ts = parse_posix_time(f'{now.month:02d}{now.day:02d}{now.hour:02d}{now.minute:02d}')
    assert isinstance(ts, float)
    # [[CC]YY]MMDDhhmm[.ss]
    ts = parse_posix_time('202501011200')
    assert datetime.fromtimestamp(ts).year == 2025
    ts = parse_posix_time('2501011200')
    assert datetime.fromtimestamp(ts).year == 2025
    ts = parse_posix_time('202501011200.30')
    assert datetime.fromtimestamp(ts).second == 30
    assert parse_posix_time('badformat') is None

def test_parse_date_string():
    now = time.time()
    assert abs(parse_date_string('now') - now) < 2
    assert abs(parse_date_string('1 hour ago') - (now - 3600)) < 2
    assert abs(parse_date_string('1 day ago') - (now - 86400)) < 2
    assert parse_date_string('2025-01-01 12:00:00') == datetime(2025, 1, 1, 12, 0, 0).timestamp()
    assert parse_date_string('badformat') is None

def test_touch_file_basic():
    tmpdir = tempfile.mkdtemp()
    test_file = os.path.join(tmpdir, 'testfile')
    try:
        assert touch_file(test_file)
        assert os.path.isfile(test_file)
        # Test updating times
        t = time.time() - 10000
        assert touch_file(test_file, atime=t, mtime=t)
        statinfo = os.stat(test_file)
        assert abs(statinfo.st_atime - t) < 2
        assert abs(statinfo.st_mtime - t) < 2
    finally:
        shutil.rmtree(tmpdir)

def test_touch_file_no_create():
    tmpdir = tempfile.mkdtemp()
    test_file = os.path.join(tmpdir, 'nofile')
    try:
        assert touch_file(test_file, no_create=True)
        assert not os.path.exists(test_file)
    finally:
        shutil.rmtree(tmpdir)

def run_cli(args):
    cmd = [sys.executable, os.path.abspath('touch.py')] + args
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result

def test_cli_basic():
    tmpdir = tempfile.mkdtemp()
    test_file = os.path.join(tmpdir, 'cli_file')
    try:
        result = run_cli([test_file])
        assert os.path.isfile(test_file)
        assert result.returncode == 0
    finally:
        shutil.rmtree(tmpdir)

def test_cli_no_create():
    tmpdir = tempfile.mkdtemp()
    test_file = os.path.join(tmpdir, 'cli_nofile')
    try:
        result = run_cli(['-c', test_file])
        assert not os.path.exists(test_file)
        assert result.returncode == 0
    finally:
        shutil.rmtree(tmpdir)

def test_cli_date():
    tmpdir = tempfile.mkdtemp()
    test_file = os.path.join(tmpdir, 'cli_date')
    try:
        result = run_cli(['-d', '2025-01-01 12:00:00', test_file])
        assert os.path.isfile(test_file)
        statinfo = os.stat(test_file)
        assert datetime.fromtimestamp(statinfo.st_mtime).year == 2025
        assert result.returncode == 0
    finally:
        shutil.rmtree(tmpdir)

def test_cli_t():
    tmpdir = tempfile.mkdtemp()
    test_file = os.path.join(tmpdir, 'cli_t')
    try:
        result = run_cli(['-t', '202501011200', test_file])
        assert os.path.isfile(test_file)
        statinfo = os.stat(test_file)
        assert datetime.fromtimestamp(statinfo.st_mtime).year == 2025
        assert result.returncode == 0
    finally:
        shutil.rmtree(tmpdir)

def test_cli_help():
    result = run_cli(['--help'])
    assert 'Usage:' in result.stdout
    assert result.returncode == 0

def test_cli_version():
    result = run_cli(['--version'])
    assert 'touch (Python port of GNU coreutils)' in result.stdout
    assert result.returncode == 0

def test_cli_missing_operand():
    result = run_cli([])
    assert 'missing file operand' in result.stderr
    assert result.returncode == 1
