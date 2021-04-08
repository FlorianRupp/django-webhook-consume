import json
import logging
import os
import subprocess

import requests
from django.conf import settings as s
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators import http, csrf

from django_webhook_consume.helper import check_hash, check_branch

logger = logging.getLogger('django_webhook_consume')
logger.setLevel(logging.DEBUG)
logging.basicConfig(filename="django_webhook_consume.log",
                    filemode='a',
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


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
        logging.error("no config for this hook.")
        return HttpResponse(status=400)
    try:
        secret = os.environ[cfg["secret_key_name"]]
    except KeyError:
        logging.error("key is not configured through env.")
        return HttpResponse(status=400)

    try:
        github_header = request.META[cfg["github_header_name"]]
    except KeyError:
        logging.error("Configured github header not in request.")
        return HttpResponse(status=400)

    if check_hash(secret, payload, github_header) is True:
        if check_branch(json.loads(payload), cfg["branch"]):
            logger.info(f"Script {cfg['script']} executing...")
            requests.post(s.EXECUTION_SERVER, data={'command': cfg['script']})
            logger.info("Script execution sent.")
            return HttpResponse()
        else:
            logging.error("Hashes matched, but event is not configured.")
            return HttpResponse(status=404)
    else:
        logging.warning("Hashes did not match!")
        return HttpResponseForbidden()
