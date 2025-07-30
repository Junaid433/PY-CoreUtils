import subprocess
import sys
import os
import socket

SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'hostname.py'))


def run_cli(args):
    """Helper to run the hostname script with arguments."""
    result = subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True)
    return result


def test_print_hostname():
    """Test printing the current hostname."""
    result = run_cli([])
    assert result.returncode == 0
    expected_hostname = socket.gethostname()
    assert result.stdout.strip() == expected_hostname


def test_set_hostname_permission_error():
    """Test setting the hostname, which should fail without root privileges."""
    result = run_cli(['new-hostname'])
    # This should fail because tests are not run as root
    assert result.returncode == 1
    assert 'Operation not permitted' in result.stderr or 'Function not implemented' in result.stderr


def test_extra_operand():
    """Test hostname with an extra operand."""
    result = run_cli(['name1', 'name2'])
    assert result.returncode == 1
    assert 'extra operand' in result.stderr


def test_help():
    """Test the --help option."""
    result = run_cli(['--help'])
    assert result.returncode == 0
    assert 'Usage: hostname' in result.stdout


def test_version():
    """Test the --version option."""
    result = run_cli(['--version'])
    assert result.returncode == 0
    assert 'hostname (Python port of GNU coreutils)' in result.stdout
