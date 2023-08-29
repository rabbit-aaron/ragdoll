from __future__ import annotations

import inspect
import os
import typing
from types import ModuleType, SimpleNamespace

from ragdoll import env
from ragdoll.env import BaseEnvEntry
from ragdoll.errors import ImproperlyConfigured


def _dir_factory(module: ModuleType) -> typing.Callable[[], list[str]]:
    def dir_() -> typing.Generator[str, None, None]:
        mock_owner = SimpleNamespace(source=os.environ, case_sensitive=True)
        errors = []
        for name, value in module.__dict__.items():
            if isinstance(value, BaseEnvEntry):
                value.__set_name__(mock_owner, name)  # type: ignore[arg-type]
                try:
                    result = value.__get__(mock_owner, None)  # type: ignore[arg-type]

                except ImproperlyConfigured as improperly_configured:
                    errors.append(improperly_configured)
                else:
                    setattr(module, name, result)
            yield name
        if errors:
            raise ImproperlyConfigured(errors)

    return lambda: list(dir_())


class ModuleNotFound(Exception):
    pass


def _configure(frame_idx: int) -> None:
    frame = inspect.stack()[frame_idx].frame
    module = inspect.getmodule(frame)

    if not module:
        raise ModuleNotFound

    if not getattr(module, "_dir_patched", False):
        setattr(module, "__dir__", _dir_factory(module))
        setattr(module, "_dir_patched", True)

    del frame


def configure() -> None:
    return _configure(frame_idx=2)


class DjangoEnvEntryMixin:
    def __init__(self, *args, **kwargs):
        _configure(frame_idx=2)
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
