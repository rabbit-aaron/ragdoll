from ragdoll.django import DjangoEnvSetting
from ragdoll.env import StrEnv


def test_django_env_setting_export(monkeypatch):
    global FOO
    monkeypatch.setenv("FOO", "BAR")

    class MyDjangoEnvSetting(DjangoEnvSetting):
        FOO = StrEnv()  # export=True

    assert "FOO" in globals()
    assert FOO == "BAR"
    assert MyDjangoEnvSetting.FOO == "BAR"
    del FOO


def test_django_env_setting_no_export(monkeypatch):
    global FOO
    monkeypatch.setenv("FOO", "BAR")

    class MyDjangoEnvSetting(DjangoEnvSetting):
        FOO = StrEnv(export=False)

    assert "FOO" not in globals()
    assert MyDjangoEnvSetting.FOO == "BAR"
