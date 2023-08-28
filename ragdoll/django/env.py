from __future__ import annotations

import inspect
import os
import sys
import typing
from types import SimpleNamespace, ModuleType

from ragdoll import base, env
from ragdoll.env import EnvSetting, BaseEnvEntry


class DjangoSettingMixin:
    default_export = True

    @classmethod
    def configure_entry(cls, entry: base.BaseEntry, name: str, value: str):
        if entry.extra_kwargs.get("export", cls.default_export):
            setattr(sys.modules[cls.__module__], name, value)


class DjangoEnvSetting(DjangoSettingMixin, EnvSetting):
    pass


def dir_factory(module: ModuleType) -> typing.Callable[[], list[str]]:
    def dir_() -> typing.Generator[str, None, None]:
        mock_owner = SimpleNamespace(source=os.environ, case_sensitive=True)
        for name, value in module.__dict__.items():
            if isinstance(value, BaseEnvEntry):
                value.__set_name__(mock_owner, name)  # type: ignore
                setattr(module, name, value.__get__(mock_owner, None))  # type: ignore
            yield name

    return lambda: list(dir_())


class DjangoEnvEntryMixin:
    def __init__(self, *args, **kwargs):
        frame = inspect.stack()[1].frame
        module = inspect.getmodule(frame)
        if not getattr(module, "_dir_patched", False):
            module.__dir__ = dir_factory(module)
            module._dir_patched = True

        del frame
        super().__init__(*args, **kwargs)


class Int(DjangoEnvEntryMixin, env.Int):
    pass


class Str(DjangoEnvEntryMixin, env.Str):
    pass


class Bool(DjangoEnvEntryMixin, env.Bool):
    pass


if typing.TYPE_CHECKING:
    Int = int  # type: ignore # noqa: F811
    Bool = bool  # type: ignore # noqa: F811
    Str = str  # type: ignore # noqa: F811
