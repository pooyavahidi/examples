import os
import subprocess

prog = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./my_cli.py")


def test_exists():
    assert os.path.isfile(prog)


def test_version_option():
    for flag in ["--version"]:
        res = subprocess.run([prog, flag], check=False, capture_output=True)
        assert res.returncode == 0
        assert res.stdout.rstrip().decode() == "v0.0.0"


def test_no_handler():
    res = subprocess.run([prog, "nohandler"], check=False, capture_output=True)
    assert res.returncode != 0
    assert res.stderr.rstrip().decode().startswith("No handler")


def test_deployer_logs_verbose_option():
    cmd = [prog, "deployer", "logs"]
    for flag in ["-v", "--verbose"]:
        cmd.append(flag)
        res = subprocess.run(cmd, check=False, capture_output=True)
        assert res.returncode == 0
        assert res.stdout.rstrip().decode() == "deployer logs verbose"


def test_no_option():
    res = subprocess.run([prog], check=False, capture_output=True)
    assert res.returncode != 0
    assert res.stdout.rstrip().decode().startswith("usage:")


def test_deployer_logs_error_within_command():
    cmd = [prog, "deployer", "logs", "-l", "0"]
    res = subprocess.run(cmd, check=False, capture_output=True)
    assert res.returncode == 2
    assert res.stderr
    assert not res.stdout


def test_deployer_logs():
    cmd = [prog, "deployer", "logs"]
    for flag in ["-l", "--limit"]:
        cmd.extend([flag, "3"])
        res = subprocess.run(cmd, check=True, capture_output=True)
        assert res.returncode == 0
        assert res.stdout.rstrip().decode() == "3"


def test_deployer_logs_error_on_command_creation():
    cmd = [prog, "deployer", "no-command"]
    res = subprocess.run(cmd, check=False, capture_output=True)
    assert res.returncode != 0


def test_show_args():
    cmd = [prog, "show", "args"]
    res = subprocess.run(cmd, check=False, capture_output=True)
    assert res.returncode == 0
    assert res.stdout.rstrip().decode() == "test"


def test_show_dir():
    cmd = [prog, "show", "dir"]
    res = subprocess.run(cmd, check=False, capture_output=True)
    assert res.returncode == 0
