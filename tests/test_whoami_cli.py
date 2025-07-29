import subprocess
import sys
import os
import pwd

SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'whoami.py'))

def run_cli(args):
    result = subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True)
    return result

def test_whoami_basic():
    result = run_cli([])
    assert result.returncode == 0
    expected = pwd.getpwuid(os.geteuid()).pw_name
    assert result.stdout.strip() == expected

def test_whoami_help():
    result = run_cli(['--help'])
    assert 'Usage:' in result.stdout
    assert result.returncode == 0

def test_whoami_version():
    result = run_cli(['--version'])
    assert 'whoami (GNU coreutils)' in result.stdout
    assert result.returncode == 0

def test_whoami_extra_operand():
    result = run_cli(['extra'])
    assert 'extra operand' in result.stderr
    assert result.returncode == 1
