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
from ragdoll import env

class MySetting(env.EnvSetting):
    # default_value is a positional argument, so it can be omitted
    WORKER_COUNT = env.Int(default_value=3)
    HOST_NAME = env.Str("localhost")
    
    # no default value specified, if the environment variable SECRET_KEY is not set, it will raise ragdoll.errors.ImproperlyConfigured
    SECRET_KEY = env.Str()
    DEBUG = env.Bool(False)
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
Django load settings by running `dir(<SETTINGS_MODULE>)`,
I took advantage of that and magically inject a `__dir__` method to the settings module.
This makes things simpler for Django settings

```python
# settings.py
from ragdoll.django import env

# Keep in mind that all Django settings must be in upper case,
# otherwise Django will not load them
DEBUG = env.Bool(False)
DOMAIN_NAME = env.Str("example.com")
MAX_CONNECTION_COUNT = env.Int()
    
# if you do not want django to pick up the settings
# simply use lower case variables
db_host = env.Str()
db_name = env.Str()
db_user = env.Str()
db_password = env.Str()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': db_name,
        'USER': db_user,
        'PASSWORD': db_password,
        'HOST': db_host,
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
### IMPORTANT: THIS WILL NOT WORK
Since the injected `__dir__` function only look at global variables, nested settings will not work,
You must assign the settings to a global variable first, then use it in nested settings.

```python
from ragdoll.django import env

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.Str(),
        'USER': env.Str(),
        'PASSWORD': env.Str(),
        'HOST': env.Str(),
        'PORT': '5432',
    }
}
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
from ragdoll.base import BaseEntry

class CommaSeparatedEnv(BaseEntry):
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

from ragdoll.django import env
from ragdoll.env import BaseEnvEntry


# Note the DjangoEnvEntryMixin here, that's where the __dir__ injection happens
# it's very important to include it if this is intended for Django settings.
class DbUrl(env.DjangoEnvEntryMixin, BaseEnvEntry):
    """This field turns database URL into a Django DATABASES setting dictionary"""
    def to_python(self, value:str) -> dict:
        return {"default": dj_database_url.parse(value)}
```
To use it:
```python
# settings.py
from my_fields import DbUrl

DATABASES = DbUrl("postgres://ragdoll:meow@localhost:5432/ragdoll")
```

## Validations

```python
# my_fields.py
import dj_database_url
from ragdoll.base import BaseEntry
from ragdool.errors import ImproperlyConfigured

class HexIntEnv(BaseEntry):
    """This field turns a hex string into an integer"""
    def to_python(self, value:str) -> int:
        try:
            return int(value, base=16)
        except ValueError:
            # if ImproperlyConfigured is raised, ragdoll will collect all of the errors
            # and re-raise them all at once
            raise ImproperlyConfigured(f"{self.name} must be a hexadecimal value, e.g. '0x1000'")
```
