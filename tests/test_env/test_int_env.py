import pytest

from ragdoll import env, errors


def test_int_env(monkeypatch):
    monkeypatch.setenv("DECIMAL", "1000")
    monkeypatch.setenv("HEXADECIMAL", "FF")

    class MyEnvSetting(env.EnvSetting):
        DECIMAL = env.Int()
        HEXADECIMAL = env.Int(base=16)

    assert MyEnvSetting.DECIMAL == 1000
    assert MyEnvSetting.HEXADECIMAL == 255


def test_bad_int_env(monkeypatch):
    monkeypatch.setenv("DECIMAL", "ABC")

    with pytest.raises(errors.ImproperlyConfigured):

        class MyEnvSettings(env.EnvSetting):
            DECIMAL = env.Int()


def test_int_env_name():
    class MyEnvSetting(env.EnvSetting):
        FOO = env.Int(0)

    assert MyEnvSetting.__dict__["FOO"].name == "FOO"


def test_process_default_value():
    class MyEnvSetting(env.EnvSetting):
        FOO = env.Int("0", process_default_value=True)

    assert MyEnvSetting.FOO == 0


def test_process_default_value_choices():
    class MyEnvSetting(env.EnvSetting):
        FOO = env.Int("0", process_default_value=True, choices=[0])


def test_process_default_value_choices_error():
    with pytest.raises(AssertionError):

        class MyEnvSetting(env.EnvSetting):
            FOO = env.Int("0", process_default_value=True, choices=[1])
