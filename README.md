### Installation

    $ pip3 install git+https://github.com/kadena-io/pypact.git

### Environment Variables

pypact configuration use environment variables: **PUB_KEY**, **PRIV_KEY**, **PACT_SERVER** so make sure you export this variables or you can use override*config(pub_key, priv_key, pact_server) method in the \_config.py* file.

## Usage

Prepare pact code, sign it and send to pact server:

```python
from pypact import api
from pypact.adapters import CommandFactory


code = CommandFactory(
	"<function_name",
	"<module_name>(optional)",
	"**<parameters>"
).build_code()
# Output of the code
print(code)

# Send request and listen for the executed command
result = api.send_and_listen(code)
print(result)
```

You can request to _/local_, _/send_ and _/listen_ endpoint using methods in _api.py_
