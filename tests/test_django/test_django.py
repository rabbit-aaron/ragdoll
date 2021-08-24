from ragdoll.django import DjangoEnvSetting
from ragdoll.env import StrEnv


def test_django_env_setting_export(monkeypatch):
    monkeypatch.setenv("FOO", "BAR")

    class MyDjangoEnvSetting(DjangoEnvSetting):
        FOO = StrEnv(export=True)

    assert "FOO" in globals()
    assert FOO == "BAR"  # noqa: F821
