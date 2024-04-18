import pytest

from ragdoll import errors
from ragdoll.env import EnvSetting, StrEnv


def test_str_env(monkeypatch):
    monkeypatch.setenv("FOO", "FOO")
    monkeypatch.setenv("BAR", "BAR")

    class MyEnvSetting(EnvSetting):
        FOO = StrEnv()
        bar = StrEnv(None)

    assert MyEnvSetting.FOO == "FOO"
    assert MyEnvSetting.bar is None


def test_str_env_default_not_in_choice():
    with pytest.raises(AssertionError):
        StrEnv(default_value="foo", choices={"hello", "world"})


def test_str_env_choices(monkeypatch):
    monkeypatch.setenv("FOO", "FOO")

    class MyEnvSetting(EnvSetting):
        FOO = StrEnv(choices={"FOO"})


def test_str_env_not_set_within_choices(monkeypatch):
    monkeypatch.setenv("FOO", "FOO")

    with pytest.raises(errors.ImproperlyConfigured):

        class MyEnvSetting(EnvSetting):
            FOO = StrEnv(choices={"ABC"})


def test_str_env_not_found_no_default():
    with pytest.raises(errors.ImproperlyConfigured):

        class MyEnvSetting(EnvSetting):
            FOO = StrEnv()


def test_str_env_name():
    class MyEnvSetting(EnvSetting):
        FOO = StrEnv("")

    assert MyEnvSetting.__dict__["FOO"].name == "FOO"


def test_str_env_callable_default():
    class MyEnvSetting(EnvSetting):
        FOO = StrEnv(lambda: "")

    assert MyEnvSetting.FOO == ""
