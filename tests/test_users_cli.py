import subprocess
import sys
import os
import struct
import pytest

SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'users.py'))

# Constants from the users.py script for creating a fake utmp file
USER_PROCESS = 7
DEAD_PROCESS = 8
UTMP_STRUCT_FORMAT = 'hi32s4s32s256shhiii4i20x'
UTMP_STRUCT_SIZE = struct.calcsize(UTMP_STRUCT_FORMAT)


def run_cli(args):
    """Helper to run the users script with arguments."""
    env = os.environ.copy()
    return subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True, env=env)


def create_fake_utmp_file(file_path):
    """Helper to create a fake utmp file for testing."""
    with open(file_path, "wb") as f:
        # Record 1: A valid user
        f.write(struct.pack(UTMP_STRUCT_FORMAT, USER_PROCESS, 123, b'tty1', b'id1', b'root\0', b'host1', 0, 0, 0, 0, 0, 0, 0, 0, 0))
        # Record 2: Another valid user
        f.write(struct.pack(UTMP_STRUCT_FORMAT, USER_PROCESS, 456, b'tty2', b'id2', b'guest\0', b'host2', 0, 0, 0, 0, 0, 0, 0, 0, 0))
        # Record 3: A duplicate user session
        f.write(struct.pack(UTMP_STRUCT_FORMAT, USER_PROCESS, 789, b'pts/0', b'id3', b'root\0', b'host3', 0, 0, 0, 0, 0, 0, 0, 0, 0))
        # Record 4: A non-user process (should be ignored)
        f.write(struct.pack(UTMP_STRUCT_FORMAT, DEAD_PROCESS, 111, b'tty3', b'id4', b'reboot\0', b'host4', 0, 0, 0, 0, 0, 0, 0, 0, 0))
        # Record 5: A user with a long name
        f.write(struct.pack(UTMP_STRUCT_FORMAT, USER_PROCESS, 222, b'tty4', b'id5', b'a_very_long_username_here\0', b'host5', 0, 0, 0, 0, 0, 0, 0, 0, 0))
    return str(file_path)


# --- UNIX-specific Tests ---

@pytest.mark.skipif(sys.platform == 'win32', reason="UNIX-specific test for utmp file")
def test_users_unix_basic(tmp_path):
    """Test basic functionality on UNIX with a fake utmp file."""
    fake_utmp = create_fake_utmp_file(tmp_path / "utmp")
    result = run_cli([fake_utmp])
    assert result.returncode == 0
    # Output should be sorted alphabetically
    assert result.stdout.strip() == "a_very_long_username_here guest root root"


@pytest.mark.skipif(sys.platform == 'win32', reason="UNIX-specific test")
def test_users_unix_no_file():
    """Test error message when the specified file does not exist."""
    result = run_cli(['/no/such/file/exists'])
    assert result.returncode == 1
    assert "cannot open '/no/such/file/exists': No such file or directory" in result.stderr


@pytest.mark.skipif(sys.platform == 'win32', reason="UNIX-specific test")
def test_users_unix_empty_file(tmp_path):
    """Test that an empty utmp file produces no output."""
    empty_file = tmp_path / "empty_utmp"
    empty_file.touch()
    result = run_cli([str(empty_file)])
    assert result.returncode == 0
    assert result.stdout == ""


@pytest.mark.skipif(sys.platform == 'win32', reason="UNIX-specific test")
def test_users_unix_permission_denied(tmp_path):
    """Test permission denied error on UNIX."""
    no_access_file = tmp_path / "no_access"
    no_access_file.touch()
    os.chmod(no_access_file, 0o000)
    result = run_cli([str(no_access_file)])
    assert result.returncode == 1
    assert "Permission denied" in result.stderr
    # Cleanup
    os.chmod(no_access_file, 0o644)


# --- Windows-specific Tests ---

@pytest.mark.skipif(sys.platform != 'win32', reason="Windows-specific test")
def test_users_windows_from_cli(tmp_path, monkeypatch):
    """Test Windows version by executing a fake 'query.cmd' from the PATH."""
    fake_cli_path = tmp_path / "fake_cli"
    fake_cli_path.mkdir()
    monkeypatch.setenv("PATH", str(fake_cli_path), prepend=os.pathsep)

    query_cmd_content = (
        '@echo off\n'
        'echo  USERNAME              SESSIONNAME        ID  STATE   IDLE TIME  LOGON TIME\n'
        'echo >user2                 console             1  Active      none   1/1/2024 10:00 AM\n'
        'echo  user1                 rdp-tcp#0           2  Active          .  1/1/2024 11:00 AM\n'
    )
    (fake_cli_path / "query.cmd").write_text(query_cmd_content)

    result = run_cli([])
    assert result.returncode == 0
    # The script sorts the users
    assert result.stdout.strip() == "user1 user2"


@pytest.mark.skipif(sys.platform != 'win32', reason="Windows-specific test")
def test_users_windows_fallback_on_cli_error(tmp_path, monkeypatch):
    """Test Windows fallback when the 'query' command fails."""
    fake_cli_path = tmp_path / "fake_cli"
    fake_cli_path.mkdir()
    monkeypatch.setenv("PATH", str(fake_cli_path), prepend=os.pathsep)

    # Create a query.cmd that returns an error, triggering the fallback.
    (fake_cli_path / "query.cmd").write_text('@echo off\nexit /b 1')

    # We still mock os.getlogin for a deterministic test of the fallback.
    monkeypatch.setattr(os, 'getlogin', lambda: "fallback_user")

    result = run_cli([])
    assert result.returncode == 0
    assert result.stdout.strip() == "fallback_user"


@pytest.mark.skipif(sys.platform != 'win32', reason="Windows-specific test")
def test_users_windows_fallback_to_environ(tmp_path, monkeypatch):
    """Test Windows final fallback to USERNAME environment variable."""
    fake_cli_path = tmp_path / "fake_cli"
    fake_cli_path.mkdir()
    monkeypatch.setenv("PATH", str(fake_cli_path), prepend=os.pathsep)

    # Create a query.cmd that returns an error
    (fake_cli_path / "query.cmd").write_text('@echo off\nexit /b 1')

    # Mock getlogin to fail, triggering the next fallback
    monkeypatch.setattr(os, 'getlogin', lambda: (_ for _ in ()).throw(OSError))
    monkeypatch.setenv('USERNAME', 'env_user')
    result = run_cli([])
    assert result.returncode == 0
    assert result.stdout.strip() == "env_user"


@pytest.mark.skipif(sys.platform != 'win32', reason="Windows-specific test")
def test_users_windows_ignore_file_arg():
    """Test that the file argument is ignored on Windows with a warning."""
    result = run_cli(['some/file/path'])
    assert "warning: FILE argument is ignored on Windows" in result.stderr


# --- Generic Tests ---

def test_extra_operand():
    """Test error message for an extra operand."""
    result = run_cli(['file1', 'file2'])
    assert result.returncode == 1
    assert "extra operand 'file2'" in result.stderr


def test_help():
    """Test the --help option."""
    result = run_cli(['--help'])
    assert result.returncode == 0
    assert 'Usage: users [OPTION]... [FILE]' in result.stdout


def test_version():
    """Test the --version option."""
    result = run_cli(['--version'])
    assert result.returncode == 0
    assert 'users (Python port of GNU coreutils)' in result.stdout
