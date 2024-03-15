import abc
from typing import Any, Mapping, Optional, Type, Union

from ragdoll import errors


class BaseEntry(abc.ABC):

    _NOT_SET = object()
    DEFAULT_EXPORT = False
    source: Mapping

    def __init__(
        self,
        default_value: Any = _NOT_SET,
        *,
        name: str = None,
        choices: Optional[Union[list, tuple, set]] = None,
        process_default_value: bool = False,
        **kwargs,
    ):
        self._name = name
        self._process_default_value = process_default_value
        self._default_value = default_value

        if choices and self._default is not self._NOT_SET:
            assert (
                self._default in choices
            ), f"`default_value` must be one of {choices!r}"

        self._choices = choices
        self.extra_kwargs = kwargs

    @property
    def _default(self) -> Any:
        if self._process_default_value:
            return self.to_python(self._default_value)
        return self._default_value

    @property
    def name(self):
        return self._name

    @abc.abstractmethod
    def to_python(self, value: Any) -> Any:  # pragma: no cover
        raise NotImplementedError

    def get_raw_value(self) -> Any:
        try:
            return self.source[self._name]
        except KeyError as key_error:
            raise errors.EnvNotFound from key_error

    def __set_name__(self, owner: Type["BaseSetting"], name: str):
        if not self._name:
            self._name = name

        self.source = owner.source

    def __get__(self, instance: "BaseSetting", owner: Type["BaseSetting"]):
        try:
            raw_setting_value = self.get_raw_value()
        except errors.EnvNotFound as env_not_found:
            if self._default is self._NOT_SET:
                raise errors.ImproperlyConfigured(
                    f"{self._name} setting was not set"
                ) from env_not_found

            return self._default

        converted_value = self.to_python(raw_setting_value)

        if self._choices and converted_value not in self._choices:
            raise errors.ImproperlyConfigured(
                f"{self._name} setting must be set to one of {self._choices!r}"
            )

        return converted_value


class SettingMeta(abc.ABCMeta):
    def __init__(cls: Type["BaseSetting"], *args, **kwargs):
        super().__init__(*args, **kwargs)

        if cls.auto_configure:
            cls.configure()


class BaseSetting(metaclass=SettingMeta):

    auto_configure = True
    source: Mapping

    @classmethod
    def configure_entry(cls, entry: BaseEntry, name: str, value: str):
        pass

    @classmethod
    def configure(cls):
        result = {}
        errors_ = []

        for name, value in cls.__dict__.items():
            if isinstance(value, BaseEntry):
                try:
                    result[name] = getattr(cls, name)
                    cls.configure_entry(value, name, result[name])
                except errors.ImproperlyConfigured as exc:
                    errors_.append(exc)

        if errors_:
            raise errors.ImproperlyConfigured(errors_)

        return result
