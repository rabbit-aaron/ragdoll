from types import ModuleType

from ragdoll.django import env


def test_django_dir_patched(mocker):
    module = ModuleType("settings")
    mocker.patch("inspect.getmodule", return_value=module)
    module.MYVAR = env.Int(5)
    dir(module)
    assert module._dir_patched


def test_django_int_env(monkeypatch, mocker):
    monkeypatch.setenv("MYVAR", "50")
    module = ModuleType("settings")
    mocker.patch("inspect.getmodule", return_value=module)
    module.MYVAR = env.Int()
    dir(module)
    assert module.MYVAR == 50


def test_django_str_env(monkeypatch, mocker):
    monkeypatch.setenv("BAO", "ragdoll")
    module = ModuleType("settings")
    mocker.patch("inspect.getmodule", return_value=module)
    module.BAO = env.Str()
    dir(module)
    assert module.BAO == "ragdoll"


def test_django_bool_env(monkeypatch, mocker):
    monkeypatch.setenv("BAO", "True")
    module = ModuleType("settings")
    mocker.patch("inspect.getmodule", return_value=module)
    module.BAO = env.Bool()
    dir(module)
    assert module.BAO is True
