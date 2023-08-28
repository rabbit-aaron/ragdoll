from __future__ import annotations

import functools
import os
import typing

from ragdoll import errors, utils
from ragdoll.base import BaseEntry, BaseSetting

__all__ = ["EnvSetting", "BaseEnvEntry", "Str", "Bool", "Int"]


class BaseEnvEntry(BaseEntry):
    def get_raw_value(self) -> str:
        return super().get_raw_value()

    def __set_name__(self, owner: type[EnvSetting], name: str):  # type: ignore[override]
        super().__set_name__(owner, name)
        if not owner.case_sensitive:
            self._name = name.lower()


class Str(BaseEnvEntry):
    def to_python(self, value: str) -> str:
        return value


class Int(BaseEnvEntry):
    def __init__(self, *args, base: int = 10, **kwargs):
        self._base = base
        super().__init__(*args, **kwargs)

    def to_python(self, value: str) -> int:
        try:
            return int(value, self._base)
        except ValueError as value_error:
            raise errors.ImproperlyConfigured(
                f"Cannot convert {self._name} to integer"
            ) from value_error


class Bool(BaseEnvEntry):
    TRUE_VALUES = {"true", "1", "yes"}
    FALSE_VALUES = {"false", "0", "no", ""}

    def to_python(self, value: str) -> bool:
        value = value.lower()

        if value in self.TRUE_VALUES:
            return True

        if value in self.FALSE_VALUES:
            return False

        raise errors.ImproperlyConfigured(
            f"Value for {self._name} must be one of "
            f"{(self.TRUE_VALUES | self.FALSE_VALUES)!r}"
        )


class EnvSetting(BaseSetting):
    case_sensitive = True

    @utils.classproperty
    @functools.cache
    def source(cls) -> typing.Mapping[str, str]:
        if cls.case_sensitive:
            return os.environ
        else:
            return {k.lower(): v for k, v in os.environ.items()}


if typing.TYPE_CHECKING:  # pragma: no cover
    Int = int  # type: ignore # noqa: F811
    Bool = bool  # type: ignore # noqa: F811
    Str = str  # type: ignore # noqa: F811
