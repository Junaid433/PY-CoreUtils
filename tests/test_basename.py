import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from basename import remove_suffix, strip_trailing_slashes, is_absolute_path, get_file_system_prefix_len, base_name


def test_remove_suffix():
    assert remove_suffix('filename.txt', '.txt') == 'filename'
    assert remove_suffix('filename.txt', '.md') == 'filename.txt'
    assert remove_suffix('file.txt.txt', '.txt') == 'file.txt'
    assert remove_suffix('txt', 'txt') == 'txt'
    assert remove_suffix('file', '') == 'file'
    assert remove_suffix('', '.txt') == ''


def test_strip_trailing_slashes():
    assert strip_trailing_slashes('folder/') == 'folder'
    assert strip_trailing_slashes('folder////') == 'folder'
    assert strip_trailing_slashes('/') == '/'
    assert strip_trailing_slashes('C:\\') == 'C:\\'
    assert strip_trailing_slashes('C:/folder/') == 'C:/folder'


def test_is_absolute_path():
    import platform
    assert is_absolute_path('/usr/bin') is True
    if platform.system() == 'Windows':
        assert is_absolute_path('C:/Windows') is True
    else:
        assert is_absolute_path('C:/Windows') is False
    assert is_absolute_path('C:') is True
    assert is_absolute_path('folder/file') is False


def test_get_file_system_prefix_len():
    assert get_file_system_prefix_len('C:/Windows') == 2
    assert get_file_system_prefix_len('D:') == 2
    assert get_file_system_prefix_len('/usr/bin') == 0
    assert get_file_system_prefix_len('folder/file') == 0


def test_base_name():
    assert base_name('/usr/bin/python') == 'python'
    assert base_name('folder/file.txt') == 'file.txt'
    assert base_name('/') == '/'
    assert base_name('//') == '//'
    assert base_name('') == '.'
    assert base_name('C:/Windows') == 'Windows'
    assert base_name('C:') == 'C:'
