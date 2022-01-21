import pytest

from ragdoll import errors
from ragdoll.env import EnvSetting, IntEnv


def test_int_env(monkeypatch):
    monkeypatch.setenv("DECIMAL", "1000")
    monkeypatch.setenv("HEXADECIMAL", "FF")

    class MyEnvSetting(EnvSetting):
        DECIMAL = IntEnv()
        HEXADECIMAL = IntEnv(base=16)

    assert MyEnvSetting.DECIMAL == 1000
    assert MyEnvSetting.HEXADECIMAL == 255


def test_bad_int_env(monkeypatch):
    monkeypatch.setenv("DECIMAL", "ABC")

    with pytest.raises(errors.ImproperlyConfigured):

        class MyEnvSettings(EnvSetting):
            DECIMAL = IntEnv()


def test_int_env_name():
    class MyEnvSetting(EnvSetting):
        FOO = IntEnv(0)

    assert MyEnvSetting.__dict__["FOO"].name == "FOO"


def test_process_default_value():
    class MyEnvSetting(EnvSetting):
        FOO = IntEnv("0", process_default_value=True)

    assert MyEnvSetting.FOO == 0
