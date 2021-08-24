class RagdollError(Exception):
    pass


class ImproperlyConfigured(RagdollError, ValueError):
    pass


class EnvNotFound(RagdollError, LookupError):
    pass
