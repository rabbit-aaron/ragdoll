from __future__ import annotations

import inspect
import os
import sys
import typing
from functools import lru_cache
from types import SimpleNamespace
from typing import Any

from ragdoll import base, env
from ragdoll.env import EnvSetting


class DjangoSettingMixin:
    default_export = True

    @classmethod
    def configure_entry(cls, entry: base.BaseEntry, name: str, value: str):
        if entry.extra_kwargs.get("export", cls.default_export):
            setattr(sys.modules[cls.__module__], name, value)


class DjangoEnvSetting(DjangoSettingMixin, EnvSetting):
    pass


def dir_factory(f_globals: dict[str, Any]) -> callable[[], list[str]]:
    @lru_cache(maxsize=None)
    def dir_() -> list[str]:
        ret = []
        for k, v in tuple(f_globals.items()):
            if isinstance(v, DjangoEnvEntryMixin):
                mock_owner = SimpleNamespace(source=os.environ, case_sensitive=True)
                v.__set_name__(mock_owner, k)
                f_globals[k] = v.__get__(mock_owner, None)
            ret.append(k)
        return ret

    return dir_


class DjangoEnvEntryMixin:
    def __init__(self, *args, **kwargs):
        frame = inspect.stack()[1].frame
        module = inspect.getmodule(frame)
        if not getattr(module, "_dir_patched", False):
            module.__dir__ = dir_factory(frame.f_globals)
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
