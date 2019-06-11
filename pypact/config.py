import os

PACT_SERVER = os.environ.get("PACT_SERVER")
PUB_KEY = os.environ.get("PUB_KEY")
PRIV_KEY = os.environ.get("PRIV_KEY")


def override_config(pub_key, priv_key, pact_server):
    globals().update({ "PACT_SERVER": pact_server })
    globals().update({"PUB_KEY": pub_key})
    globals().update({"PRIV_KEY": priv_key})
