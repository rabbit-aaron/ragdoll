import pytest

from ragdoll import errors
from ragdoll.env import EnvSetting, BoolEnv


def test_bool_env(monkeypatch):
    monkeypatch.setenv("y1", "YES")
    monkeypatch.setenv("y2", "yes")
    monkeypatch.setenv("y3", "1")
    monkeypatch.setenv("y4", "true")

    monkeypatch.setenv("n1", "no")
    monkeypatch.setenv("n2", "0")
    monkeypatch.setenv("n3", "FALSE")
    monkeypatch.setenv("n4", "")

    class MyEnvSettings(EnvSetting):
        y1 = BoolEnv()
        y2 = BoolEnv()
        y3 = BoolEnv()
        y4 = BoolEnv()

        n1 = BoolEnv()
        n2 = BoolEnv()
        n3 = BoolEnv()
        n4 = BoolEnv()

    assert MyEnvSettings.y1 is True
    assert MyEnvSettings.y2 is True
    assert MyEnvSettings.y3 is True
    assert MyEnvSettings.y4 is True

    assert MyEnvSettings.n1 is False
    assert MyEnvSettings.n2 is False
    assert MyEnvSettings.n3 is False
    assert MyEnvSettings.n4 is False


def test_bad_bool_env(monkeypatch):
    monkeypatch.setenv("FOO", "HEHE")

    with pytest.raises(errors.ImproperlyConfigured):

        class MyEnvSetting(EnvSetting):
            FOO = BoolEnv()
