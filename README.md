### Installation
	
	$ pip3 install git+https://github.com/kadena-io/pypact.git

### Environment Variables

pypact configuration use environment variables: **PUB_KEY**, **PRIV_KEY**, **PACT_SERVER** so make sure you export this variables or you can hard code them into the *config.py* file.

## Usage

Prepare pact code, sign it and send to pact server:

```python
from pypact import api
from pypact.adapters import BasePactAdapter


code = BasePactAdapter.build_code(
	"<module_name>",
	"<function_name",
	"<keyset>" or ""
)
# Output of the code
print(code)

# Send request and listen for the executed command
result = api.send_and_listen(code, "<keyset>")
print(result)
```

You can request to */local*, */send* and */listen* endpoint using methods in *api.py*
 
