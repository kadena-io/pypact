import datetime
import hashlib
import json

import ed25519


class BasePactAdapter:
    @staticmethod
    def generate_code_hash_and_sign(pact_code, pub_key, priv_key):
        """Generate hash of pact code and signs it.

        :param pact_code: The dictionary of Pact yaml file
        :param pub_key: Public key of signing key
        :param priv_key: Private key of signing key
        :return: Returns tuple of hash of pact code and signed hash.
        """
        pact_code = bytes(pact_code, encoding="utf8")
        hash2b = hashlib.blake2b()
        hash2b.update(pact_code)
        sk = ed25519.keys.SigningKey(bytes(priv_key, encoding="utf8"))
        signing_key = priv_key + pub_key
        sk.vk_s = bytes.fromhex(pub_key)
        sk.sk_s = bytes.fromhex(signing_key)

        return hash2b.hexdigest(), sk.sign(hash2b.digest()).hex()

    @classmethod
    def build_code(cls, module_name, func_name, keyset, **kwargs):
        """It calls CommandFactory class in order to produce
        Pact command.

        :param module_name: The name of pact module which contains
        function name
        :param func_name: The name of function to be executed
        :param keyset: Keyset to be used by function
        :param kwargs: Additional parameters for pact function arguments
        :return: Returns pact command
        """
        return CommandFactory(module_name, func_name, keyset, **kwargs).create()

    @staticmethod
    def build_request(pact_code, pub_key, priv_key):
        test_data = "arbitrary user data"
        nonce = str(datetime.datetime.now())
        cmd = {
            "address": None,
            "payload": {
                "exec": {
                    "data": {"testdata": test_data, "issuer-admin-keyset": [pub_key]},
                    "code": pact_code,
                }
            },
            "nonce": nonce,
        }

        pact_cmd = json.dumps(cmd)
        hash_code, sig = BasePactAdapter.generate_code_hash_and_sign(
            pact_cmd, pub_key, priv_key
        )

        cmds = {
            "cmds": [
                {
                    "hash": hash_code,
                    "sigs": [{"sig": sig, "scheme": "ED25519", "pubKey": pub_key}],
                    "cmd": pact_cmd,
                }
            ]
        }
        return json.dumps(cmds)


class CommandFactory:
    """Pact command generator

    Methods:
        create: It is a generic method that produces pact commands.
    """

    def __init__(self, module_name, function_name, keyset, **kwargs):
        """ Initiate instance variables.

        :param module_name: The name of pact module which contains
        function name
        :param function_name: The name of function to be executed
        :param keyset: Provided keyset for the transaction
        :param kwargs: Additional parameters for pact function arguments
        """
        self.module_name = module_name
        self.function_name = function_name
        self.kwargs = kwargs
        self.keyset = keyset

    def create(self):
        """ Generate pact command.

        :return: Return pact command as a string
        """
        pact_command = f"(use '{self.module_name}) ({self.function_name}"

        for val in self.kwargs.values():
            param = str(val[2:]) if val[:2] == "/i" else '"' + val + '"'
            pact_command += " " + param

        return pact_command + " " + self.keyset + ")"
