import pytest

from ragdoll import env, errors


def test_str_env_case_sensitive(monkeypatch):
    monkeypatch.setenv("FOO", "FOO")
    monkeypatch.setenv("BAR", "BAR")

    class MyEnvSetting(env.EnvSetting):
        FOO = env.Str()
        bar = env.Str(None)

    assert MyEnvSetting.FOO == "FOO"
    assert MyEnvSetting.bar is None


def test_str_env_case_insensitive(monkeypatch):
    monkeypatch.setenv("FOO", "FOO")
    monkeypatch.setenv("BAR", "BAR")

    class MyEnvSetting(env.EnvSetting):
        case_sensitive = False

        FOO = env.Str()
        bar = env.Str()

    assert MyEnvSetting.FOO == "FOO"
    assert MyEnvSetting.bar == "BAR"


def test_str_env_default_not_in_choice():
    with pytest.raises(AssertionError):
        env.Str(default_value="foo", choices={"hello", "world"})


def test_str_env_choices(monkeypatch):
    monkeypatch.setenv("FOO", "FOO")

    class MyEnvSetting(env.EnvSetting):
        FOO = env.Str(choices={"FOO"})


def test_str_env_not_set_within_choices(monkeypatch):
    monkeypatch.setenv("FOO", "FOO")

    with pytest.raises(errors.ImproperlyConfigured):

        class MyEnvSetting(env.EnvSetting):
            FOO = env.Str(choices={"ABC"})


def test_str_env_not_found_no_default():
    with pytest.raises(errors.ImproperlyConfigured):

        class MyEnvSetting(env.EnvSetting):
            FOO = env.Str()


def test_str_env_name():
    class MyEnvSetting(env.EnvSetting):
        FOO = env.Str("")

    assert MyEnvSetting.__dict__["FOO"].name == "FOO"
