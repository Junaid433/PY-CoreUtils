import subprocess
import sys
import os
import time
from datetime import datetime

SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'date.py'))

def run_cli(args, input_text=None):
    return subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True, input=input_text)

def test_default_output():
    result = run_cli([])
    assert result.returncode == 0
    # Should contain year and weekday
    now = datetime.now().strftime('%Y')
    assert now in result.stdout
    assert any(day in result.stdout for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

def test_custom_format():
    result = run_cli(['+%Y-%m-%d'])
    assert result.returncode == 0
    assert datetime.now().strftime('%Y-%m-%d') in result.stdout

def test_date_option():
    result = run_cli(['-d', '2024-01-01 12:00:00', '+%Y-%m-%d %H:%M:%S'])
    assert result.returncode == 0
    assert '2024-01-01 12:00:00' in result.stdout

def test_reference_option(tmp_path):
    f = tmp_path / 'ref.txt'
    with open(f, 'w') as fp:
        fp.write('x')
    os.utime(f, (1600000000, 1600000000))
    result = run_cli(['-r', str(f), '+%s'])
    assert result.returncode == 0
    assert '1600000000' in result.stdout

def test_utc():
    result = run_cli(['-u', '+%z'])
    assert result.returncode == 0
    assert '+0000' in result.stdout or '+00' in result.stdout

def test_iso_8601():
    result = run_cli(['-I'])
    assert result.returncode == 0
    assert '-' in result.stdout

def test_rfc_3339():
    result = run_cli(['--rfc-3339', 'seconds'])
    assert result.returncode == 0
    assert '-' in result.stdout and ':' in result.stdout

def test_rfc_email():
    result = run_cli(['-R'])
    assert result.returncode == 0
    assert ',' in result.stdout and ':' in result.stdout

def test_help():
    result = run_cli(['--help'])
    assert 'Usage:' in result.stdout or 'usage:' in result.stdout.lower()
    assert result.returncode == 0

def test_version():
    result = run_cli(['--version'])
    assert 'Python port of GNU coreutils' in result.stdout or 'Junaid Rahman' in result.stdout
    assert result.returncode == 0

def test_invalid_date():
    result = run_cli(['-d', 'notadate'])
    assert result.returncode == 1
    assert 'invalid date' in result.stderr
