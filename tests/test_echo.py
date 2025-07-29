import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from echo import hextobin, is_hex_digit, process_escapes

def test_hextobin():
    assert hextobin('0') == 0
    assert hextobin('9') == 9
    assert hextobin('a') == 10
    assert hextobin('A') == 10
    assert hextobin('f') == 15
    assert hextobin('F') == 15
    assert hextobin('b') == 11
    assert hextobin('B') == 11
    assert hextobin('c') == 12
    assert hextobin('C') == 12
    assert hextobin('d') == 13
    assert hextobin('D') == 13
    assert hextobin('e') == 14
    assert hextobin('E') == 14

def test_is_hex_digit():
    for c in '0123456789abcdefABCDEF':
        assert is_hex_digit(c)
    for c in 'ghijklmnopqrstuvwxyzGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()':
        assert not is_hex_digit(c)

def test_process_escapes_basic():
    s, cont = process_escapes('hello')
    assert s == 'hello'
    assert cont is True

def test_process_escapes_newline():
    s, cont = process_escapes('line1\\nline2')
    assert s == 'line1\nline2'
    assert cont is True

def test_process_escapes_tab():
    s, cont = process_escapes('col1\\tcol2')
    assert s == 'col1\tcol2'
    assert cont is True

def test_process_escapes_bell():
    s, cont = process_escapes('bell\\a')
    assert '\a' in s
    assert cont is True

def test_process_escapes_c_ends():
    s, cont = process_escapes('stop\\cshouldnotappear')
    assert s == 'stop'
    assert cont is False

def test_process_escapes_hex():
    s, cont = process_escapes('hex\\x41')
    assert s == 'hexA'
    assert cont is True

def test_process_escapes_octal():
    s, cont = process_escapes('octal\\101')
    assert s == 'octalA'
    assert cont is True

def test_process_escapes_backslash():
    s, cont = process_escapes('slash\\\\')
    assert s == 'slash\\'
    assert cont is True
