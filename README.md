# Django Web Hook Consumer

This small app consumes web hooks from Github. It can trigger the run of a script, when a push to a specific branch of a repo was made.

## Installation

```pip install git+https://github.com/FlorianRupp/django-webhook-consume.git```

## Quick start
-----------

1. Add "django_web_hook" to your INSTALLED_APPS setting like this:
```
    INSTALLED_APPS = [
        ...,
        "django_webhook_consume" 
    ]
```
2. Include the django_web_hook URLconf in your project urls.py like this:
```
    path('hook/', include('django_webhook_consume.urls')),
```
3. No need to migrate any database.

4. Add the following config parameters to your settings.py:

* ```BRANCH```: name/path of branch to listen for push.
* ```SECRET_KEY_NAME```: name of secret key. This key must be available through environment.
* ```GITHUB_SECURE_HEADER```: Name of the Github secure header.
* ```SCRIPT```: Path to script with parameters to be executed when hook is triggered.


## Security
The payload from github is hashed added a secret key, also named salt. This application
computes this hash and compares it with the one computed by github. Only if both hashes match,
the execution is forwarded. For security reasons the value of this secret key should be configured
through environment and _not_ hardcoded. Therefore we only configure the name of the environment 
variable ```SECRET_KEY_NAME```. 