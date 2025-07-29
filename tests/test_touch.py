import sys
import os
import pytest
import time
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from touch import parse_posix_time, parse_date_string, touch_file

def test_parse_posix_time():
    now = datetime.now()
    # 8 digits: MMDDhhmm
    t = parse_posix_time('01011234')
    assert isinstance(t, float)
    # 10 digits: YYMMDDhhmm
    t = parse_posix_time('2401011234')
    assert isinstance(t, float)
    # 12 digits: CCYYMMDDhhmm
    t = parse_posix_time('202401011234')
    assert isinstance(t, float)
    # 14 digits: CCYYMMDDhhmmss
    t = parse_posix_time('20240101123456')
    assert isinstance(t, float)
    # Invalid
    assert parse_posix_time('badtime') is None
    assert parse_posix_time('') is None

def test_parse_date_string():
    now = time.time()
    assert abs(parse_date_string('now') - now) < 2
    assert abs(parse_date_string('1 hour ago') - (now - 3600)) < 2
    assert abs(parse_date_string('1 day ago') - (now - 86400)) < 2
    assert parse_date_string('2024-01-01 12:00:00') == datetime(2024, 1, 1, 12, 0, 0).timestamp()
    assert parse_date_string('bad-date') is None
    assert parse_date_string('') is None

def test_touch_file_create_and_update(tmp_path):
    f = tmp_path / 'afile.txt'
    assert touch_file(str(f)) is True
    assert f.exists()
    old_atime = f.stat().st_atime
    old_mtime = f.stat().st_mtime
    time.sleep(1)
    assert touch_file(str(f)) is True
    assert f.stat().st_atime >= old_atime
    assert f.stat().st_mtime >= old_mtime

def test_touch_file_no_create(tmp_path):
    f = tmp_path / 'nofile.txt'
    assert touch_file(str(f), no_create=True) is True
    assert not f.exists()
