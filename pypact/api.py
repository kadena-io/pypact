"""This module make requests to the endpoints of Pact API.

Functions:
    - **send:** It makes a POST Request to Pact API's 'send' endpoint.
    - **listen:** It makes a POST Request to Pact API's 'listen' \
    endpoint.
    - **local:** It makes a POST Request to Pact API's 'local' endpoint.
    - **send_and_listen:** It combines send and listen functions.
"""

import json
import requests

from .config import PACT_SERVER, PUB_KEY, PRIV_KEY
from .adapters import BasePactAdapter


def _request(endpoint, body, json_=False):
    if not json_:
        return requests.post(PACT_SERVER + endpoint, body)
    return requests.post(PACT_SERVER + endpoint, json=body)


def send(pact_command, keyset):
    """ Make a POST Request to Pact API's 'send' endpoint.

    :param pact_command: Serialised pact command
    :return: The result of POST request
    """
    req_body = json.loads(
        BasePactAdapter.build_request(
            pact_command, PUB_KEY, PRIV_KEY, keyset
        )
    )
    return _request("send", req_body, json_=True)


def listen(listen_key):
    """Make a POST Request to Pact API's 'listen' endpoint.

    :param listen_key: A key to be used for 'listen' endpoint body
    :return: The result of POST request
    """
    return _request("listen", json.dumps({"listen": listen_key}))


def local(listen_key):
    """Make a POST Request to Pact API's 'local' endpoint.

    :param listen_key: A key to be used for 'local' endpoint body
    :return: The result of POST request
    """
    return _request("local", json.dumps({"listen": listen_key}))


def send_and_listen(pact_command, keyset):
    """Call 'send' and 'listen' functions, respectively.

    :param pact_command: Serialised pact command
    :return: The result of POST request
    """
    resp = json.loads(send(pact_command, keyset).text)
    listen_response_text = listen(resp["response"]["requestKeys"].pop()).text
    response = json.loads(listen_response_text)["response"]

    if "data" in response["result"]:
        return response["result"]["data"]
    elif "error" in response["result"]:
        return response["result"]["detail"]

    return response["result"]
