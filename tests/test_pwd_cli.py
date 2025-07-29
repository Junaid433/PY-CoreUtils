import subprocess
import sys
import os

SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'pwd.py'))

def run_cli(args, env=None):
    return subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True, env=env)

def test_default_physical():
    result = run_cli([])
    assert result.returncode == 0
    assert os.path.realpath(os.getcwd()) in result.stdout.strip()

def test_logical():
    env = os.environ.copy()
    env['PWD'] = '/tmp'
    # Only works if /tmp is current dir
    os.chdir('/tmp')
    result = run_cli(['-L'], env=env)
    assert result.returncode == 0
    assert '/tmp' in result.stdout.strip()
    os.chdir('/')

def test_physical():
    result = run_cli(['-P'])
    assert result.returncode == 0
    assert os.path.realpath(os.getcwd()) in result.stdout.strip()

def test_posixly_correct():
    env = os.environ.copy()
    env['POSIXLY_CORRECT'] = '1'
    env['PWD'] = '/tmp'
    os.chdir('/tmp')
    result = run_cli([], env=env)
    assert result.returncode == 0
    assert '/tmp' in result.stdout.strip()
    os.chdir('/')

def test_help():
    result = run_cli(['--help'])
    assert 'Usage:' in result.stdout or 'usage:' in result.stdout.lower()
    assert result.returncode == 0

def test_version():
    result = run_cli(['--version'])
    assert 'Python port of GNU coreutils' in result.stdout or 'Jim Meyering' in result.stdout
    assert result.returncode == 0

def test_non_option_args():
    result = run_cli(['foo', 'bar'])
    assert 'ignoring non-option arguments' in result.stderr
    assert result.returncode == 0
