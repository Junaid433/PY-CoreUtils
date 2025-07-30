import subprocess
import sys
import os
import re

SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'hostid.py'))


def run_cli(args):
    """Helper to run the hostid script with arguments."""
    result = subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True)
    return result


def test_basic_hostid():
    """Test basic hostid command."""
    result = run_cli([])
    assert result.returncode == 0
    # The output should be an 8-digit hexadecimal string
    assert re.match(r'^[a-f0-9]{8}\n?$', result.stdout)


def test_extra_operand():
    """Test hostid with an extra operand."""
    result = run_cli(['extra'])
    assert result.returncode == 1
    assert 'extra operand' in result.stderr


def test_help():
    """Test the --help option."""
    result = run_cli(['--help'])
    assert result.returncode == 0
    assert 'Usage: hostid' in result.stdout


def test_version():
    """Test the --version option."""
    result = run_cli(['--version'])
    assert result.returncode == 0
    assert 'hostid (Python port of GNU coreutils)' in result.stdout
