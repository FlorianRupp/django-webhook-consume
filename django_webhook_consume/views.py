import json
import os

from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators import http, csrf

from django.conf import settings as s
from django_webhook_consume.helper import check_hash, check_branch


@http.require_POST
@csrf.csrf_exempt
def consume_web_hook(request):
    """
    Trigger on configured web hook. If called the hash of a given secret and received payload ist built. This hash is
    compared with received control hash. If hashes match it is checked if the hook matched the branch.
    If so the configured script is executed.
    """
    payload = request.body
    if check_hash(os.environ[s.SECRET_KEY_NAME], payload, request.META[s.GITHUB_SECURE_HEADER]) is True:
        if check_branch(json.loads(payload), s.BRANCH):
            print("Run script here")
            os.system(s.SCRIPT)
        else:
            print("Hashes matched, but event is not configured.")
        return HttpResponse()
    else:
        print("Hashes did not match!")
        return HttpResponseForbidden()
