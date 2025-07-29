import subprocess
import sys
import os

SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'echo.py'))

def run_cli(args, env=None):
    result = subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True, env=env)
    return result

def test_basic_echo():
    result = run_cli(['hello', 'world'])
    assert result.stdout == 'hello world\n'
    assert result.returncode == 0

def test_no_newline():
    result = run_cli(['-n', 'no', 'newline'])
    assert result.stdout == 'no newline'
    assert result.returncode == 0

def test_escape_enabled():
    result = run_cli(['-e', 'line1\\nline2'])
    assert result.stdout == 'line1\nline2\n'
    assert result.returncode == 0

def test_escape_disabled():
    result = run_cli(['-E', 'line1\\nline2'])
    assert result.stdout == 'line1\\nline2\n'
    assert result.returncode == 0

def test_help():
    result = run_cli(['--help'])
    assert 'Usage:' in result.stdout
    assert result.returncode == 0

def test_version():
    result = run_cli(['--version'])
    assert 'echo (Python port of GNU coreutils)' in result.stdout
    assert result.returncode == 0

def test_escape_c_stops_output():
    result = run_cli(['-e', 'stop\\cshouldnotappear'])
    assert result.stdout == 'stop'
    assert result.returncode == 0

def test_posixly_correct_env():
    env = os.environ.copy()
    env['POSIXLY_CORRECT'] = '1'
    result = run_cli(['-e', 'line1\\nline2'], env=env)
    # With POSIXLY_CORRECT, -e is not treated as an option, but as a string
    assert result.stdout == '-e line1\nline2\n'
    assert result.returncode == 0
