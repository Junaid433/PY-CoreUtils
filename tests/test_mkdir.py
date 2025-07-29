import pytest
import os
import sys
import shutil
import tempfile
from mkdir import parse_mode, make_directory
import subprocess

def test_parse_mode_octal():
    assert parse_mode('755') == 0o755
    assert parse_mode('0777') == 0o777
    assert parse_mode('644') == 0o644
    assert parse_mode('') is None
    assert parse_mode('invalid') is None

def test_parse_mode_symbolic():
    assert parse_mode('u+rwx') & 0o700 == 0o700
    assert parse_mode('g+rx') & 0o070 == 0o070
    assert parse_mode('o+rx') & 0o007 == 0o007
    assert parse_mode('a+rw') & 0o666 == 0o666
    assert parse_mode('u=rw,g=r,o=') & 0o777 == 0o640
    assert parse_mode('u+s') & 0o4000 == 0o4000
    assert parse_mode('g+s') & 0o2000 == 0o2000
    assert parse_mode('o+t') & 0o1000 == 0o1000
    assert parse_mode('u-x') & 0o700 == 0o600
    assert parse_mode('a-x') & 0o777 == 0o666

def test_make_directory_basic():
    tmpdir = tempfile.mkdtemp()
    test_dir = os.path.join(tmpdir, 'testdir')
    try:
        assert make_directory(test_dir)
        assert os.path.isdir(test_dir)
    finally:
        shutil.rmtree(tmpdir)

def test_make_directory_parents():
    tmpdir = tempfile.mkdtemp()
    nested_dir = os.path.join(tmpdir, 'a/b/c')
    try:
        assert make_directory(nested_dir, parents=True)
        assert os.path.isdir(nested_dir)
    finally:
        shutil.rmtree(tmpdir)

def test_make_directory_exists_ok():
    tmpdir = tempfile.mkdtemp()
    try:
        assert make_directory(tmpdir, exists_ok=True)
    finally:
        shutil.rmtree(tmpdir)

def run_cli(args):
    cmd = [sys.executable, os.path.abspath('mkdir.py')] + args
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result

def test_cli_basic():
    tmpdir = tempfile.mkdtemp()
    test_dir = os.path.join(tmpdir, 'cli_test')
    try:
        result = run_cli([test_dir])
        assert os.path.isdir(test_dir)
        assert result.returncode == 0
    finally:
        shutil.rmtree(tmpdir)

def test_cli_parents():
    tmpdir = tempfile.mkdtemp()
    nested_dir = os.path.join(tmpdir, 'a/b/c')
    try:
        result = run_cli(['-p', nested_dir])
        assert os.path.isdir(nested_dir)
        assert result.returncode == 0
    finally:
        shutil.rmtree(tmpdir)

def test_cli_mode():
    tmpdir = tempfile.mkdtemp()
    test_dir = os.path.join(tmpdir, 'modedir')
    try:
        result = run_cli(['-m', '700', test_dir])
        assert os.path.isdir(test_dir)
        assert (os.stat(test_dir).st_mode & 0o777) == 0o700
        assert result.returncode == 0
    finally:
        shutil.rmtree(tmpdir)

def test_cli_verbose():
    tmpdir = tempfile.mkdtemp()
    test_dir = os.path.join(tmpdir, 'vdir')
    try:
        result = run_cli(['-v', test_dir])
        assert os.path.isdir(test_dir)
        assert 'created directory' in result.stdout
        assert result.returncode == 0
    finally:
        shutil.rmtree(tmpdir)

def test_cli_help():
    result = run_cli(['--help'])
    assert 'Usage:' in result.stdout
    assert result.returncode == 0

def test_cli_version():
    result = run_cli(['--version'])
    assert 'mkdir (Python port of GNU coreutils)' in result.stdout
    assert result.returncode == 0

def test_cli_missing_operand():
    result = run_cli([])
    assert 'missing operand' in result.stderr
    assert result.returncode == 1

def test_cli_invalid_mode():
    tmpdir = tempfile.mkdtemp()
    test_dir = os.path.join(tmpdir, 'badmodedir')
    try:
        result = run_cli(['-m', 'badmode', test_dir])
        assert 'invalid mode' in result.stderr
        assert result.returncode == 1
    finally:
        shutil.rmtree(tmpdir)
