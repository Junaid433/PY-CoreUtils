import sys
import os
import pytest
from unittest import mock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mkdir import parse_mode, make_directory

def test_parse_mode_octal():
    assert parse_mode('755') == 0o755
    assert parse_mode('0777') == 0o777
    assert parse_mode('644') == 0o644
    assert parse_mode('') is None
    assert parse_mode('invalid') is None

def test_parse_mode_symbolic():
    assert (parse_mode('u+rwx') & 0o700) == 0o700
    assert (parse_mode('g+rx') & 0o070) == 0o070  # group rx bits set
    assert (parse_mode('o+rx') & 0o007) == 0o007  # other rx bits set
    assert (parse_mode('a+r') & 0o444) == 0o444
    assert (parse_mode('u-x') & 0o100) == 0
    assert (parse_mode('g-w') & 0o020) == 0
    assert (parse_mode('o=rw') & 0o007) == 0o006
    assert (parse_mode('u+s') & 0o4000) == 0o4000
    assert (parse_mode('g+s') & 0o2000) == 0o2000
    assert (parse_mode('o+t') & 0o1000) == 0o1000
    assert (parse_mode('u=rw,g=rx,o=r') & 0o777) == 0o654

def test_make_directory_success(tmp_path):
    d = tmp_path / 'testdir'
    assert make_directory(str(d)) is True  # Returns True on success
    assert d.exists() and d.is_dir()

def test_make_directory_exists(tmp_path):
    d = tmp_path / 'testdir2'
    d.mkdir()
    assert make_directory(str(d), exists_ok=True) is True

def test_make_directory_permission_error(monkeypatch):
    def raise_perm(*a, **kw):
        raise PermissionError
    monkeypatch.setattr(os, 'mkdir', raise_perm)
    assert make_directory('nope') is False
