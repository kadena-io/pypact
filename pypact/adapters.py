import datetime
import hashlib
import json
import ed25519

class BasePactAdapter:
    @staticmethod
    def generate_hash_code_and_sign(pact_command, pub_key, priv_key):
        """Generate hash of pact code and signs it.

        :param pact_command: The dictionary of Pact yaml file
        :param pub_key: Public key of signing key
        :param priv_key: Private key of signing key
        :return: Returns tuple of hash of pact code and signed hash.
        """
        pact_command_in_bytes = bytes(pact_command, encoding="utf8")
        hash2b = hashlib.blake2b()
        hash2b.update(pact_command_in_bytes)
        sk = ed25519.keys.SigningKey(bytes(priv_key, encoding="utf8"))
        signing_key = priv_key + pub_key
        sk.vk_s = bytes.fromhex(pub_key)
        sk.sk_s = bytes.fromhex(signing_key)

        return hash2b.hexdigest(), sk.sign(hash2b.digest()).hex()

    @staticmethod
    def make_command_json_body(pact_command, pub_key, keyset_name):
        cmd = {
            "address": None,
            "payload": {
                "exec": {
                    "data": {
                        keyset_name: [pub_key],
                    },
                    "code": pact_command,
                }
            },
            "nonce": str(datetime.datetime.now()),
        }
        return cmd

    @staticmethod
    def add_command_to_commands(cmd, pub_key, priv_key):
        pact_cmd = json.dumps(cmd)
        hash_code, sig = BasePactAdapter.generate_hash_code_and_sign(
            pact_cmd, pub_key, priv_key
        )
        cmds_body = {
            "hash": hash_code,
            "sigs": [{"sig": sig, "scheme": "ED25519", "pubKey": pub_key}],
            "cmd": pact_cmd,
        }
        return cmds_body

    @staticmethod
    def build_request(pact_command, pub_key, priv_key, keyset_name):
        cmd = BasePactAdapter.make_command_json_body(pact_command, pub_key,
                                                     keyset_name)
        cmds = {
            "cmds": [BasePactAdapter.add_command_to_commands(cmd, pub_key,
                                                             priv_key)]
        }
        return json.dumps(cmds)

    @staticmethod
    def build_local_request(pact_command, pub_key, priv_key, keyset_name):
        cmd = BasePactAdapter.make_command_json_body(pact_command, pub_key,
                                                     keyset_name)
        cmds = BasePactAdapter.add_command_to_commands(cmd, pub_key, priv_key)

        return json.dumps(cmds)

    @staticmethod
    def build_batch_command_request_body(pact_commands, pub_key, priv_key,
                                         keyset_name):
        cmds = {
            "cmds": []}

        for single_command in pact_commands:
            cmd = BasePactAdapter.make_command_json_body(single_command,
                                                         pub_key,
                                                         keyset_name)
            single_cmd = BasePactAdapter.add_command_to_commands(cmd, pub_key,
                                                                 priv_key)
            cmds["cmds"].append(single_cmd)

        return json.dumps(cmds)


class CommandFactory:
    """Pact command generator

    Methods:
        create: It is a generic method that produces pact commands.
    """

    def __init__(self, function_name, module_name="", **kwargs):
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

    def build_code(self):
        """ Generate pact command.

        :return: Return pact command as a string
        """
        if self.module_name == "":
            pact_command = f"({self.function_name}"
        else:
            pact_command = f"({self.module_name}.{self.function_name}"

        for val in self.kwargs.values():
            pact_command += " " + val

        command = pact_command
        return command + ")"
