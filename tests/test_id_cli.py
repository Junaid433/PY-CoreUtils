import subprocess
import sys
import os
import pwd
import grp
import pytest

ID_SCRIPT = os.path.join(os.path.dirname(__file__), '../src/id.py')
PYTHON_EXEC = sys.executable

def run_id_cli(*args):
    cmd = [PYTHON_EXEC, ID_SCRIPT] + list(args)
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result

def test_id_cli_default():
    result = run_id_cli()
    assert result.returncode == 0
    # Should contain uid= and gid= for current user
    assert f"uid={os.getuid()}" in result.stdout
    assert f"gid={os.getgid()}" in result.stdout

@pytest.mark.parametrize("flag,expected", [
    ("-u", str(os.getuid())),
    ("-g", str(os.getgid())),
])
def test_id_cli_uid_gid(flag, expected):
    result = run_id_cli(flag)
    assert result.returncode == 0
    assert result.stdout.strip() == expected

def test_id_cli_user_name():
    result = run_id_cli("-un")
    assert result.returncode == 0
    assert result.stdout.strip() == pwd.getpwuid(os.getuid()).pw_name

def test_id_cli_group_name():
    result = run_id_cli("-gn")
    assert result.returncode == 0
    assert result.stdout.strip() == grp.getgrgid(os.getgid()).gr_name

def test_id_cli_groups_numbers():
    result = run_id_cli("-G")
    assert result.returncode == 0
    groups = os.getgroups()
    output = set(map(int, result.stdout.strip().split()))
    assert set(groups) <= output  # output may include primary group

def test_id_cli_groups_names():
    result = run_id_cli("-Gn")
    assert result.returncode == 0
    group_names = [grp.getgrgid(gid).gr_name for gid in os.getgroups() if gid in [g.gr_gid for g in grp.getgrall()]]
    output = result.stdout.strip().split()
    for name in group_names:
        assert name in output

def test_id_cli_help():
    result = run_id_cli("--help")
    assert result.returncode == 0
    assert "Usage:" in result.stdout

def test_id_cli_version():
    result = run_id_cli("--version")
    assert result.returncode == 0
    assert "Python port of GNU coreutils" in result.stdout

def test_id_cli_invalid_user():
    result = run_id_cli("nouserdoesnotexist")
    assert result.returncode == 1
    assert "no such user" in result.stderr

def test_id_cli_conflicting_options():
    result = run_id_cli("-u", "-g")
    assert result.returncode == 1
    assert "cannot print 'only' of more than one choice" in result.stderr
