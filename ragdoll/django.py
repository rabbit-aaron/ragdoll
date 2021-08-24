import sys

from ragdoll import base
from ragdoll.env import EnvSetting


class DjangoSettingMixin:
    @classmethod
    def configure_entry(cls, entry: base.BaseEntry, name: str, value: str):
        if entry.extra_kwargs.get("export"):
            setattr(sys.modules[cls.__module__], name, value)


class DjangoEnvSetting(DjangoSettingMixin, EnvSetting):
    pass
