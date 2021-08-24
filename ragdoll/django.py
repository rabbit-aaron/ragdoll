import sys

from ragdoll import base
from ragdoll.env import EnvSetting


class DjangoSettingMixin:
    default_export = True

    @classmethod
    def configure_entry(cls, entry: base.BaseEntry, name: str, value: str):
        if entry.extra_kwargs.get("export", cls.default_export):
            setattr(sys.modules[cls.__module__], name, value)


class DjangoEnvSetting(DjangoSettingMixin, EnvSetting):
    pass
