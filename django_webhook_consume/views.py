import json
import os

from django.conf import settings as s
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators import http, csrf

from django_webhook_consume.helper import check_hash, check_branch


@http.require_POST
@csrf.csrf_exempt
def consume_web_hook(request, hook_id):
    """
    Trigger on configured web hook (hook_id). If called the hash of a given secret and received payload ist built. This
    hash is compared with received control hash. If hashes match it is checked if the hook matched the branch.
    If so the configured script is executed.
    """
    payload = request.body
    try:
        cfg = s.WEB_HOOK[hook_id]
    except KeyError:
        print("no config for this hook.")
        return HttpResponse(status=400)
    try:
        secret = os.environ[cfg["secret_key_name"]]
    except KeyError:
        print("key is not configured through env.")
        return HttpResponse(status=400)

    try:
        github_header = request.META[cfg["github_header_name"]]
    except KeyError:
        print("Configured github header not in request.")
        return HttpResponse(status=400)

    if check_hash(secret, payload, github_header) is True:
        if check_branch(json.loads(payload), cfg["branch"]):
            print("Run script here")
            os.system(cfg["script"])
        else:
            print("Hashes matched, but event is not configured.")
        return HttpResponse()
    else:
        print("Hashes did not match!")
        return HttpResponseForbidden()
