from __future__ import annotations

import inspect
import os
import typing
from types import ModuleType, SimpleNamespace

from ragdoll import env
from ragdoll.env import BaseEnvEntry


def dir_factory(module: ModuleType) -> typing.Callable[[], list[str]]:
    def dir_() -> typing.Generator[str, None, None]:
        mock_owner = SimpleNamespace(source=os.environ, case_sensitive=True)
        for name, value in module.__dict__.items():
            if isinstance(value, BaseEnvEntry):
                value.__set_name__(mock_owner, name)  # type: ignore[arg-type]
                setattr(module, name, value.__get__(mock_owner, None))  # type: ignore[arg-type]
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


if typing.TYPE_CHECKING:  # pragma: no cover
    Int = int  # type: ignore # noqa: F811
    Bool = bool  # type: ignore # noqa: F811
    Str = str  # type: ignore # noqa: F811
