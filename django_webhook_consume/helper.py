import hmac
from hashlib import sha256


def check_hash(secret, payload, extern_hash):
    """
    Checking if configured secret and payload match the external hash.
    :param secret: Secret key.
    :param payload: Payload from web hook.
    :param extern_hash: Sha256 hash from web hook.
    :return: True if hashes matched, False otherwise.
    """
    local_hash = "sha256=" + hmac.new(secret.encode("utf8"), payload, sha256).hexdigest()
    result = hmac.compare_digest(local_hash, extern_hash)
    if result is False:
        print("SHA256 local", local_hash)
        print("SHA256 extern", extern_hash)
    return result


def check_branch(payload, branch):
    """
    Check if a push was on configured branch.
    :param payload: Payload from web hook.
    :param branch: Name of branch to trigger action on.
    :return: True if push was on configured branch, False otherwise.
    """
    if "ref" in payload:
        if payload["ref"] == branch:
            return True
    return False
