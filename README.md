# Why the name?
Coming up with a good name that's not used in PyPI is hard, and my cat happens to be next to me when I initialise this project, hence the name.
# Installation
```bash
$ pip install ragdoll
```
# Introduction
Ragdoll is a small library that allows you to manage environment variables in your project easily. It allows you to convert environment variables into Python objects easily.

The project also provided an extension for integrations with Django settings files.

Ragdoll aims to solve one problem and one problem only, with no external dependencies. It's design to be extensible so adding new features on it would be very easy, there are some examples below.

# Getting started
```python
# settings.py
from ragdoll.env import EnvSetting, IntEnv, StrEnv, BoolEnv

class MySetting(EnvSetting):
    # default_value is a positional argument, so it can be omitted
    WORKER_COUNT = IntEnv(default_value=3)
    HOST_NAME = StrEnv("localhost")
    
    # no default value specified, if the environment variable SECRET_KEY is not set, it will raise ragdoll.errors.ImproperlyConfigured
    SECRET_KEY = StrEnv()
    DEBUG = BoolEnv(False)
```

Then to access these variables
```python
# assuming these environment variables are set
# WORKER_COUNT=50
# SECRET_KEY=meow
# DEBUG=1
from settings import MySetting

# types will be converted automatically
MySetting.WORKER_COUNT # 50
MySetting.HOST_NAME # 'localhost' (environment variable not set, default value is used)
MySetting.DEBUG # True
MySetting.SECRET_KEY # 'meow'
```
# Django

```python
# settings.py
from ragdoll.django import DjangoEnvSetting
from ragdoll.env import BoolEnv, StrEnv, IntEnv

class MySetting(DjangoEnvSetting):
    # These variables will be exposed as a module (global) variable automatically
    # Django will pick them up like any other settings variables
    # Keep in mind that all Django settings must be in upper case,
    # otherwise Django will not load them
    DEBUG = BoolEnv(False)
    DOMAIN_NAME = StrEnv("example.com")
    # after v0.4.0 we support callable default
    EXTRA_DOMAIN = StrEnv(lambda: "www.example.com")
    
    MAX_CONNECTION_COUNT = IntEnv()
    
    # if export=False, this variable will not be automatically exported to the module
    # so you cannot directly access it via django.conf.settings
    # this could be useful if you need this value as a part of some other settings
    DB_HOST = StrEnv(export=False)
    DB_NAME = StrEnv(export=False)
    DB_USER = StrEnv(export=False)
    DB_PASSWORD = StrEnv(export=False)


# The settings that are not exported can be access via the MySetting class
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': MySetting.DB_NAME,
        'USER': MySetting.DB_USER,
        'PASSWORD': MySetting.DB_PASSWORD,
        'HOST': MySetting.DB_HOST,
        'PORT': '5432',
    }
}
```
To load settings
```python
# assuming these environment variables are set
# DEBUG=1
# MAX_CONNECTION_COUNT=50
# DB_HOST=localhost
# DB_NAME=ragdoll
# DB_USER=ragdoll
# DB_PASSWORD=meow

from django.conf import settings

settings.DEBUG # True
settings.DOMAIN_NAME # 'example.com'  (environment variable not set, default value is used)
settings.MAX_CONNECTION_COUNT # 50

settings.DATABASES
# {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'ragdoll',
#         'USER': 'ragdoll',
#         'PASSWORD': 'meow',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
```

# Using ragdoll with python-dotenv
```python
# settings.py
from dotenv import load_dotenv
from ragdoll.env import EnvSetting, BoolEnv

# just ensure load_dotenv is called before the class is defined
load_dotenv()

class MySettings(EnvSetting):
    DEBUG = BoolEnv()
```
alternatively, you can turn off `auto_configure` to defer the loading of variables

```python
from dotenv import load_dotenv
from ragdoll.env import EnvSetting, BoolEnv

class MySetting(EnvSetting):
    auto_configure = False
    DEBUG = BoolEnv()

load_dotenv()
MySetting.configure()
```
# Recipes

### Turning a comma separated string into a list of strings

```python
# my_fields.py
from typing import List
from ragdoll.env import BaseEnvEntry

class CommaSeparatedEnv(BaseEnvEntry):
    """This field turns comma separated values into a list of strings"""
    def to_python(self, value:str) -> List[str]:
        return value.split(",")
```
To use it:

```python
# assuming the this environment variables is set
# ALLOWED_HOSTS=example.com,example.org

from ragdoll.env import EnvSetting
from my_fields import CommaSeparatedEnv

class MyEnvSetting(EnvSetting):
    ALLOWED_HOSTS = CommaSeparatedEnv()

MyEnvSetting.ALLOWED_HOSTS # ['example.com', 'example.org']
```
### Setup Django database using dj_database_url

```python
# my_fields.py
import dj_database_url
frmo ragdoll.env import BaseEnvEntry

class DbUrlEnv(BaseEnvEntry):
    """This field turns database URL into a Django DATABASES setting dictionary"""
    def to_python(self, value:str) -> dict:
        return {"default": dj_database_url.parse(value)}
```
To use it:
```python
# settings.py
from ragdoll.django import DjangoEnvSetting
from my_fields import DbUrlEnv

class MySetting(DjangoEnvSetting):
    DATABASES = DbUrlEnv("postgres://ragdoll:meow@localhost:5432/ragdoll")
```

## Validations

```python
# my_fields.py
import dj_database_url
from ragdoll.env import BaseEnvEntry
from ragdool.errors import ImproperlyConfigured

class HexIntEnv(BaseEnvEntry):
    """This field turns a hex string into an integer"""
    def to_python(self, value:str) -> int:
        try:
            return int(value, base=16)
        except ValueError:
            # if ImproperlyConfigured is raised, ragdoll will collect all of the errors
            # and re-raise them all at once
            raise ImproperlyConfigured(f"{self.name} must be a hexadecimal value, e.g. '0x1000'")
```
