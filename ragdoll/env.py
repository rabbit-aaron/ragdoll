import os
import typing

from ragdoll import errors
from ragdoll.base import BaseEntry, BaseSetting

__all__ = ["EnvSetting", "BaseEnvEntry", "StrEnv", "BoolEnv", "IntEnv"]


class BaseEnvEntry(BaseEntry):
    def get_raw_value(self) -> str:
        return super().get_raw_value()

    def __set_name__(self, owner: typing.Type["EnvSetting"], name: str):
        super().__set_name__(owner, name)


class StrEnv(BaseEnvEntry):
    def to_python(self, value: str) -> str:
        return value

    if typing.TYPE_CHECKING:

        def __get__(self, *args, **kwargs) -> str: ...


class IntEnv(BaseEnvEntry):
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

    if typing.TYPE_CHECKING:

        def __get__(self, *args, **kwargs) -> int: ...


class BoolEnv(BaseEnvEntry):
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

    if typing.TYPE_CHECKING:

        def __get__(self, *args, **kwargs) -> bool: ...


class EnvSetting(BaseSetting):
    source = os.environ
