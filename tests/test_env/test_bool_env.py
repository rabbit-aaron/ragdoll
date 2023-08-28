import pytest

from ragdoll import env, errors


@pytest.mark.parametrize(
    "input_value,expected",
    [
        ("YES", True),
        ("yes", True),
        ("1", True),
        ("true", True),
        ("no", False),
        ("0", False),
        ("FALSE", False),
        ("", False),
    ],
)
def test_bool_env(input_value, expected, monkeypatch):
    monkeypatch.setenv("var", input_value)

    class MyEnvSettings(env.EnvSetting):
        var = env.Bool()

    assert MyEnvSettings.var is expected


def test_bad_bool_env(monkeypatch):
    monkeypatch.setenv("FOO", "HEHE")

    with pytest.raises(errors.ImproperlyConfigured):

        class MyEnvSetting(env.EnvSetting):
            FOO = env.Bool()


def test_bool_env_name():
    class MyEnvSetting(env.EnvSetting):
        FOO = env.Bool(False)

    assert MyEnvSetting.__dict__["FOO"].name == "FOO"
