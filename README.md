# Django Web Hook Consumer

This small app consumes web hooks from Github. It can trigger the run of a script, when a push to a specific branch of
 a repo was made. Multiple web hook can be configured.

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

4. For each web hook endpoint add the following config structure to your settings.py:
This example config triggers a script if a push to the master branch was made.

```
WEB_HOOK = {
    "web-hook-id": {
        "branch": "refs/heads/master",
        "secret_key_name": "<NAME_OF_ENV_VAR>>",
        "github_header_name": "HTTP_X_HUB_SIGNATURE_256",
        "script": "shell command to execute"
}}
```

* ```branch```: name/path of branch to listen for push. Care github notation.
* ```secret_key_name```: name of secret key. This key must be available through environment.
* ```github_header_name```: Name of the Github secure header.
* ```script```: Path to script with parameters to be executed when hook is triggered.

5. Using this configuration, the URL to the web hook endpoint would be:
```yourdomain.org/hook/web-hook-id```

## Security
The payload from github is hashed added a secret key, also named salt. This application
computes this hash and compares it with the one computed by github. Only if both hashes match,
the execution is forwarded. For security reasons the value of this secret key should be configured
through environment and _not_ hardcoded. Therefore we only configure the name of the environment 
variable ```SECRET_KEY_NAME```. 