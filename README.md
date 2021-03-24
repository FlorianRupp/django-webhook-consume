# Django Web Hook Consumer

This small app consumes web hooks from Github. It can trigger the run of a script, when a push to a specific branch of a repo was made.

## Quick start
-----------

1. Add "django_web_hook" to your INSTALLED_APPS setting like this::
```
    INSTALLED_APPS = [
        ...,
        "django_webhook_consume" 
    ]
```
2. Include the django_web_hook URLconf in your project urls.py like this::
```
    path('hook/', include('django_webhook_consume.urls')),
```
3. No need to migrate any database.

4. Add the following config parameters to your settings.py:

* ```BRANCH```: name/path of branch to listen for push.
* ```SECRET_KEY_NAME```: name of secret key. This key must be available through environment.
* ```GITHUB_SECURE_HEADER```: Name of the Github secure header.
* ```SCRIPT```: Path to script with parameters to be executed when hook is triggered.