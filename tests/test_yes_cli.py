import subprocess
import sys
import os

SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'yes.py'))

def run_cli(args):
    """Helper to run the yes script with arguments."""
    return subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True)

def test_yes_default():
    """Test default 'y' output by piping to head."""
    # The command to run in the shell
    command = f'"{sys.executable}" "{SCRIPT}" | head -n 5'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    assert result.returncode == 0
    assert result.stderr == ""
    expected_output = "y\ny\ny\ny\ny\n"
    assert result.stdout == expected_output

def test_yes_custom_string():
    """Test custom string output by piping to head."""
    command = f'"{sys.executable}" "{SCRIPT}" hello world | head -n 3'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    assert result.returncode == 0
    assert result.stderr == ""
    expected_output = "hello world\nhello world\nhello world\n"
    assert result.stdout == expected_output

def test_yes_help():
    """Test the --help option."""
    result = run_cli(['--help'])
    assert result.returncode == 0
    assert 'Usage: yes [STRING]...' in result.stdout

def test_yes_version():
    """Test the --version option."""
    result = run_cli(['--version'])
    assert result.returncode == 0
    assert 'yes (Python port of GNU coreutils)' in result.stdout
