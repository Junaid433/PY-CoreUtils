import subprocess
import sys
import os
import signal

KILL = [sys.executable, os.path.join(os.path.dirname(__file__), '../src/kill.py')]

def run_kill(*args):
    return subprocess.run(KILL + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def test_help_output():
    result = run_kill('--help')
    assert result.returncode == 0
    assert 'kill: kill [-s sigspec | -n signum | -sigspec]' in result.stdout
    assert 'Exit Status:' in result.stdout

def test_version_output():
    result = run_kill('--version')
    assert result.returncode == 0
    assert 'kill (Python port of GNU coreutils)' in result.stdout

def test_list_signals():
    result = run_kill('-l')
    assert result.returncode == 0
    assert 'SIGTERM' in result.stdout or 'TERM' in result.stdout

def test_list_signals_with_number():
    result = run_kill('-l', '9')
    assert result.returncode == 0
    assert 'SIGKILL' in result.stdout or 'KILL' in result.stdout

def test_list_signals_L():
    result = run_kill('-L')
    assert result.returncode == 0
    assert 'SIGTERM' in result.stdout or 'TERM' in result.stdout

def test_table_output():
    result = run_kill('-t')
    assert result.returncode == 0
    assert 'SIGTERM' in result.stdout or 'TERM' in result.stdout
    assert '15' in result.stdout  # SIGTERM is usually 15

def test_mutual_exclusion():
    result = run_kill('-l', '-t')
    assert result.returncode != 0
    assert 'multiple signal/list/table options specified' in result.stderr

def test_missing_operand():
    result = run_kill('-s', 'TERM')
    assert result.returncode != 0
    assert 'missing operand' in result.stderr

def test_invalid_signal():
    result = run_kill('-s', 'NOSUCHSIGNAL', '1234')
    assert result.returncode != 0
    assert 'unknown signal' in result.stderr

def test_invalid_signal_number():
    result = run_kill('-n', 'notanumber', '1234')
    assert result.returncode != 0
    assert 'invalid signal number' in result.stderr

def test_short_signal_specifier():
    # -9 is SIGKILL, should error on missing operand
    result = run_kill('-9')
    assert result.returncode != 0
    assert 'missing operand' in result.stderr

def test_send_signal_to_self():
    # This should not actually kill the test process, so use harmless signal
    result = run_kill('-s', '0', str(os.getpid()))
    assert result.returncode == 0

def test_send_signal_invalid_pid():
    result = run_kill('-s', 'TERM', 'notapid')
    assert result.returncode != 0
    assert 'invalid process id' in result.stderr

def test_send_signal_unknown_pid():
    # Use a high unlikely PID
    result = run_kill('-s', 'TERM', '999999')
    # Should error, but not crash
    assert result.returncode != 0
    assert 'no such process' in result.stderr or 'permission denied' in result.stderr
