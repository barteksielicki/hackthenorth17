import json
import string
from urllib.parse import urljoin

import requests


class APIClientException(Exception):
    pass


class APIParameterException(APIClientException):
    """ raised if value provided by user using endpoint is not valid """
    pass


class APIRequestException(APIClientException):
    """ raised if something went wrong during creating request from function call """
    pass


class APIResponseException(APIClientException):
    """ raised if API response status was not 200 """

    def __init__(self, *args, **kwargs):
        self.response = kwargs.pop("response", None)
        super().__init__(*args, **kwargs)


class APIParameter:
    def __init__(self, required=False, allowed_types=None, default=None):
        self.required = required
        self.default = default
        if allowed_types and not isinstance(allowed_types, (list, tuple)):
            allowed_types = (allowed_types)
        self.allowed_types = allowed_types

    def validate(self, value):
        if value is None:
            if self.required and self.default is None:
                raise APIParameterException("This parameter is required!")
            return self.default
        if self.allowed_types and not isinstance(value, self.allowed_types):
            raise APIParameterException(f"Wrong type! {type(value)} provided, when {self.allowed_types} expected.")
        return value


class APIClient:
    """ Class representing API Client. It might be used for bootstraping API libs """

    def __init__(self, base_url, token=None, basic_auth=None, as_json=True):
        self.base_url = base_url
        self.as_json = as_json
        self.token = token
        self.basic_auth = basic_auth

    def get(self, endpoint, params=None):
        """ return function making GET requests """
        params = params or {}

        def api_call(**kwargs):
            return self._get_response(requests.get, **{
                "url": self.format_url(endpoint, kwargs),
                "params": self.get_request_params(params, kwargs)
            })

        return api_call

    def post(self, endpoint, data=None):
        """ return function making POST requests """
        data = data or {}

        def api_call(**kwargs):
            return self._get_response(requests.post, **{
                "url": self.format_url(endpoint, kwargs),
                "json" if self.as_json else "data": self.get_request_params(data, kwargs)
            })

        return api_call

    def put(self, endpoint, data=None):
        """ return function making PUT requests """
        data = data or {}

        def api_call(**kwargs):
            return self._get_response(requests.put, **{
                "url": self.format_url(endpoint, kwargs),
                "json" if self.as_json else "data": self.get_request_params(data, kwargs)
            })

        return api_call

    def _get_response(self, method, **kwargs):
        # authentication
        if self.token:
            kwargs["headers"] = {f'Authorization': f'Token {self.token}'}
        if self.basic_auth:
            kwargs["auth"] = self.basic_auth

        # request
        r = method(**kwargs)
        if r.status_code >= 400:
            raise APIResponseException(f"Unexpected API response code: {r.status_code}", response=r)
        try:
            return json.loads(r.content)
        except json.decoder.JSONDecodeError:
            raise APIResponseException("Response content is not serializable", response=r)

    def format_url(self, endpoint, kwargs_dict):
        """ extract required endpoint URL params from function kwargs """
        parameters = [f[1] for f in string.Formatter().parse(endpoint) if f[1] is not None]
        url_params = {}
        for name in parameters:
            try:
                url_params[name] = kwargs_dict.pop(name)
            except KeyError:
                raise APIClientException(
                    f"{name} URL parameter was not provided")
        return urljoin(self.base_url, endpoint.format_map(url_params))

    def get_request_params(self, params, kwargs_dict):
        """ extract params from function kwargs """
        request_params = {}
        for name, param in params.items():
            value = kwargs_dict.pop(name, None)
            try:
                value = param.validate(value)
                if value is not None:
                    request_params[name] = value
            except APIParameterException as e:
                raise APIClientException(f"Parameter {name} not valid: {e}")
        return request_params or None