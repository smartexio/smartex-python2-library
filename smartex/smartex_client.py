from smartex_exceptions import *
import smartex_key_utils as key_utils
import requests
import json
import re


class Client:

    def __init__(self, api_uri="https://smartex.io", insecure=False,
                 pem=key_utils.generate_pem(), tokens={}):

        self.uri = api_uri
        self.verify = not(insecure)
        self.pem = pem
        self.client_id = key_utils.get_sin_from_pem(pem)
        self.tokens = tokens
        self.user_agent = 'Smartex Python Client'

    def pair_pos_client(self, code):
        """
        POST /tokens
        https://smartex.io/api#resource-Tokens
        """
        if re.match("^\w{7,7}$", code) is None:
            raise SmartexArgumentError("pairing code is not legal")
        payload = {'id': self.client_id, 'pairingCode': code}
        headers = {"content-type": "application/json",
                   "accept": "application/json", "X-accept-version": "1.0.0"}
        try:
            response = requests.post(self.uri + "/tokens", verify=self.verify,
                                     data=json.dumps(payload), headers=headers)
        except Exception:
            raise SmartexConnectionError('Connection refused')
        if response.ok:
            self.tokens = self.token_from_response(response.json())
            return self.tokens
        self.response_error(response)

    def create_token(self, facade):
        """
        POST /tokens
        https://smartex.io/api#resource-Tokens
        """
        payload = {'id': self.client_id, 'facade': facade}
        headers = {"content-type": "application/json",
                   "accept": "application/json", "X-accept-version": "1.0.0"}
        try:
            response = requests.post(self.uri + "/tokens", verify=self.verify,
                                     data=json.dumps(payload), headers=headers)
        except Exception:
            raise SmartexConnectionError('Connection refused')
        if response.ok:
            self.tokens = self.token_from_response(response.json())
            return response.json()['data'][0]['pairingCode']
        self.response_error(response)

    def create_invoice(self, params):
        """
        POST /invoices
        https://smartex.io/api#resource-Invoices
        """
        self.verify_invoice_params(params['price'], params['currency'])
        payload = json.dumps(params)
        uri = self.uri + "/invoices"
        xidentity = key_utils.get_compressed_public_key_from_pem(self.pem)
        xsignature = key_utils.sign(uri + payload, self.pem)
        headers = {"content-type": "application/json",
                   "accept": "application/json", "X-Identity": xidentity,
                   "X-Signature": xsignature, "X-accept-version": "1.0.0"}
        try:
            response = requests.post(uri, data=payload, headers=headers,
                                     verify=self.verify)
        except Exception as pro:
            raise SmartexConnectionError(pro.args)
        if response.ok:
            return response.json()['data']
        self.response_error(response)

    def get_invoice(self, invoice_id):
        """
        GET /invoices/:invoiceId
        https://smartex.io/api#resource-Invoices
        """
        uri = self.uri + "/invoices/" + invoice_id
        try:
            response = requests.get(uri, verify=self.verify)
        except Exception as pro:
            raise SmartexConnectionError(pro.args)
        if response.ok:
            return response.json()['data']
        self.response_error(response)

    def verify_tokens(self):
        """
        GET /tokens
        https://smartex.io/api#resource-Tokens
        """
        xidentity = key_utils.get_compressed_public_key_from_pem(self.pem)
        xsignature = key_utils.sign(self.uri + "/tokens", self.pem)
        headers = {"content-type": "application/json",
                   "accept": "application/json", "X-Identity": xidentity,
                   "X-Signature": xsignature, "X-accept-version": '1.0.0'}
        response = requests.get(self.uri + "/tokens", headers=headers,
                                verify=self.verify)
        if response.ok:
            allTokens = response.json()['data']
            selfKeys = self.tokens.keys()
            matchedTokens = [token for token in allTokens for key in selfKeys
                             if token.get(key) == self.tokens.get(key)]
        if not matchedTokens:
            return False
        return True

    def token_from_response(self, responseJson):
        token = responseJson['data'][0]['token']
        facade = responseJson['data'][0]['facade']
        return {facade: token}
        raise SmartexSmartexError(
            '%(code)d: %(message)s' % {'code': response.status_code,
                                       'message': response.json()['error']})

    def verify_invoice_params(self, price, currency):
        if re.match("^[A-Z]{3,3}$", currency) is None:
            raise SmartexArgumentError("Currency is invalid.")
        try:
            float(price)
        except:
            raise SmartexArgumentError("Price must be formatted as a float")

    def response_error(self, response):
        raise SmartexSmartexError(
            '%(code)d: %(message)s' % {'code': response.status_code,
                                       'message': response.json()['error']})
