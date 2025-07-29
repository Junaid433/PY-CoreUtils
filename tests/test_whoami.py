import subprocess
import sys
import os
import pwd

def run_cli(args):
    cmd = [sys.executable, os.path.abspath('whoami.py')] + args
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result

def test_cli_basic():
    result = run_cli([])
    expected_user = pwd.getpwuid(os.geteuid()).pw_name
    assert result.stdout.strip() == expected_user
    assert result.returncode == 0

def test_cli_help():
    result = run_cli(['--help'])
    assert 'Usage:' in result.stdout
    assert result.returncode == 0

def test_cli_version():
    result = run_cli(['--version'])
    assert 'whoami (GNU coreutils)' in result.stdout
    assert result.returncode == 0

def test_cli_extra_operand():
    result = run_cli(['extra'])
    assert 'extra operand' in result.stderr
    assert result.returncode == 1
