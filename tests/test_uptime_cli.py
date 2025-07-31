import subprocess
import sys
import os
import pytest
import struct
import time
import re
from datetime import datetime, timedelta

SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'uptime.py'))

# Constants from users.py for creating a fake utmp file
USER_PROCESS = 7
UTMP_STRUCT_FORMAT = 'hi32s4s32s256shhiii4i20x'
UTMP_STRUCT_SIZE = struct.calcsize(UTMP_STRUCT_FORMAT)


def run_cli(args, env=None):
    """Helper to run the uptime script with arguments and a custom environment."""
    process_env = os.environ.copy()
    if env:
        process_env.update(env)
    return subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True, env=process_env)


def create_fake_utmp_file(file_path, user_count=3):
    """Creates a fake utmp file with a specified number of user sessions."""
    with open(file_path, "wb") as f:
        for i in range(user_count):
            user = f"user{i}".encode('utf-8')
            f.write(struct.pack(UTMP_STRUCT_FORMAT, USER_PROCESS, 123 + i, b'tty1', b'id1', user + b'\0', b'host1', 0, 0, 0, 0, 0, 0, 0, 0, 0))
    return str(file_path)


# --- Generic Tests ---

def test_uptime_help():
    result = run_cli(['--help'])
    assert result.returncode == 0
    assert 'Usage: uptime' in result.stdout


def test_uptime_version():
    result = run_cli(['--version'])
    assert result.returncode == 0
    assert 'uptime (Python port of GNU coreutils)' in result.stdout


def test_uptime_extra_operand():
    result = run_cli(['somefile', 'extra'])
    assert result.returncode == 1
    assert "extra operand 'extra'" in result.stderr


# --- UNIX-specific Tests ---

@pytest.mark.skipif(sys.platform == 'win32', reason="UNIX-specific test")
def test_uptime_unix_format_days(tmp_path, monkeypatch):
    """Test the full output format on UNIX for uptime > 24 hours."""
    # 1. Mock boot time: 2 days, 3 hours, 5 minutes ago
    boot_timestamp = time.time() - (2 * 86400 + 3 * 3600 + 5 * 60)
    fake_proc_stat = tmp_path / "stat"
    fake_proc_stat.write_text(f"btime {int(boot_timestamp)}\n")
    test_env = {
        '_PYCOREUTILS_TEST_PROC_STAT': str(fake_proc_stat),
        '_PYCOREUTILS_TEST_LOAD_AVG': '1.23,4.56,7.89'
    }

    # 2. Mock user count (3 users) and load average
    fake_utmp = create_fake_utmp_file(tmp_path / "utmp", 3)

    # 3. Run and assert
    result = run_cli([fake_utmp], env=test_env)
    assert result.returncode == 0
    output = result.stdout
    assert re.search(r'\d{2}:\d{2}:\d{2}', output)
    assert "up 2 days,  3:05" in output
    assert "3 users" in output
    assert "load average: 1.23, 4.56, 7.89" in output


@pytest.mark.skipif(sys.platform == 'win32', reason="UNIX-specific test")
def test_uptime_unix_format_hours(tmp_path, monkeypatch):
    """Test the full output format on UNIX for uptime < 24 hours."""
    # 1. Mock boot time: 4 hours, 15 minutes ago
    boot_timestamp = time.time() - (4 * 3600 + 15 * 60)
    fake_proc_stat = tmp_path / "stat"
    fake_proc_stat.write_text(f"btime {int(boot_timestamp)}\n")
    test_env = {
        '_PYCOREUTILS_TEST_PROC_STAT': str(fake_proc_stat),
        '_PYCOREUTILS_TEST_LOAD_AVG': '0.10,0.20,0.30'
    }

    # 2. Mock user count (1 user) and load average
    fake_utmp = create_fake_utmp_file(tmp_path / "utmp_single", 1)

    # 3. Run and assert
    result = run_cli([fake_utmp], env=test_env)
    assert result.returncode == 0
    output = result.stdout
    assert "up  4:15" in output
    assert "1 user" in output
    assert "load average: 0.10, 0.20, 0.30" in output


# --- Windows-specific Tests ---

@pytest.mark.skipif(sys.platform != 'win32', reason="Windows-specific test")
def test_uptime_windows_format(tmp_path, monkeypatch):
    """Test the full output format on Windows."""
    # 1. Mock external commands by creating fakes on the PATH
    fake_cli_path = tmp_path / "fake_cli"
    fake_cli_path.mkdir()
    monkeypatch.setenv("PATH", str(fake_cli_path), prepend=os.pathsep)

    # 2. Mock boot time via a fake 'wmic' command (1 day, 2 hours, 5 mins ago)
    boot_dt = datetime.now() - timedelta(days=1, hours=2, minutes=5)
    wmic_boottime_str = boot_dt.strftime('%Y%m%d%H%M%S')
    (fake_cli_path / "wmic.cmd").write_text(f'@echo off\necho LastBootUpTime\necho {wmic_boottime_str}.000000+000\n')

    # 3. Mock user count via a fake 'query' command (2 users)
    query_cmd_content = (
        '@echo off\n'
        'echo  USERNAME  SESSIONNAME\n'
        'echo >user1     console\n'
        'echo  user2     rdp-tcp#0\n'
    )
    (fake_cli_path / "query.cmd").write_text(query_cmd_content)

    # 4. Run and assert
    result = run_cli([])
    assert result.returncode == 0
    output = result.stdout
    assert re.search(r'\d{2}:\d{2}:\d{2}', output)
    assert "up 1 day,  2:05" in output
    assert "2 users" in output
    assert "load average" not in output  # No load average on Windows
