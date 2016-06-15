# Using the Smartex Python Client Library


## Prerequisites
You must have smartex merchant account to use this library. [Signing up for a merchant account](https://smartex.io/dashboard/signup) is free.

## Quick Start

### Basic Usage

The smartex library allows authenticating with smartex, creating invoices, and retrieving invoices.
  
#### Pairing with Smartex.io

Before pairing with smartex.io, you'll need to log in to your smartex account and navigate to /api-tokens. Generate a new pairing code and use it in the next step. You can try out various functions using the Python REPL. In this example, it's assumed that we are working against the smartex test server and have generated the pairing code "abcdefg".

    > from smartex.smartex_client import Client
    > client = Client(api_uri="https://smartex.io") #if api_uri is not passed, it defaults to "https://smartex.io"
    > client.pair_pos_client("abcdefg")

To perform a second pairing method - client-side pairing - you will need to specify the facade you want to create and call create_token(). The JSON response will include a pairing code to append to the end of the API access request URL specified in the documentation.  For example, if you wanted to create a token for the merchant facade:

    > from smartex.smartex_client import Client
    > client = Client(api_uri="https://smartex.io")
    > client.create_token("merchant")

The response will include the pairing code which you'll use for the access request URL:

```
{'data': [{'pairingExpiration': 1426204460704, 'dateCreated': 1426118060704, 'pairingCode': 'AAAAAA',
'token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'policies': [{'policy': 'id', 'params':
['xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'], 'method': 'inactive'}], 'facade': 'merchant'}]}
```

So in the example above, the URL would look like this: http://smartex.io/api-access-request?pairingCode=AAAAAA

When you nagivate to this address, you will be prompted to approve this request.  Once approved, you can use the token returned to perform any API calls needed.  To learn more about this method, see the [Smartex API documentation](https://smartex.io/api) for details.

#### To create an invoice with a paired client:

Using the same web client from the last step:

    > client.create_invoice({"price": 20, "currency": "USD", "token": client.tokens['pos']})

That will return the invoice as JSON. Other parameters can be sent, see the [Smartex API documentation](https://smartex.io/api) for details.
