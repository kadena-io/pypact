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

from . import config
from .adapters import BasePactAdapter


def _request(endpoint, body, json_=False):

    if not json_:
        return requests.post(config.PACT_SERVER + endpoint, body)
    return requests.post(config.PACT_SERVER + endpoint, json=body)


def send(pact_command, keysets, pub_key="", priv_key=""):
    """ Make a POST Request to Pact API's 'send' endpoint.

    :param pact_command: Serialised pact command
    :return: The result of POST request
    """
    pub_key = pub_key or config.PUB_KEY
    priv_key = priv_key or config.PRIV_KEY

    req_body = json.loads(
        BasePactAdapter.build_request(pact_command, pub_key, priv_key, keysets)
    )
    return _request("send", req_body, json_=True)


def send_batch_commands(pact_command_list, keyset=""):
    """ Make a POST Request to Pact API's 'send' endpoint.

    :param pact_command: Serialised pact command
    :return: The result of POST request
    """
    req_body = json.loads(
        BasePactAdapter.build_batch_command_request_body(
            pact_command_list, config.PUB_KEY, config.PRIV_KEY, keyset
        )
    )

    req_res = _request("send", req_body, json_=True)
    return req_res


def listen(listen_key):
    """Make a POST Request to Pact API's 'listen' endpoint.

    :param listen_key: A key to be used for 'listen' endpoint body
    :return: The result of POST request
    """
    return _request("listen", json.dumps({"listen": listen_key}))


def local(pact_command, keyset=""):
    """ Make a POST Request to Pact API's 'local' endpoint.

    :param pact_command: Serialised pact command
    :return: The result of POST request
    """
    req_body = json.loads(
        BasePactAdapter.build_local_request(
            pact_command, config.PUB_KEY, config.PRIV_KEY, keyset
        )
    )

    return _request("local", req_body, json_=True)


def send_and_listen(pact_command, keysets, pub_key="", priv_key=""):
    """Call 'send' and 'listen' functions, respectively.

    :param pact_command: Serialised pact command
    :return: The result of POST request
    """
    resp = json.loads(send(pact_command, keysets, pub_key, priv_key).text)
    listen_response_text = listen(resp["response"]["requestKeys"].pop()).text
    response = json.loads(listen_response_text)["response"]

    if "data" in response["result"]:
        return response["result"]["data"]
    elif "error" in response["result"]:
        return response["result"]["detail"]

    return response["result"]
