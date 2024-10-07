from datetime import datetime
import logging
import random
import requests

from simatic_s7_webserver_api.response import JsonrpcBaseResponse


class RequestConfig():
    r"""Base configuration for all requests

    :attribute: address: Address of the PLC webserver, can be either a IPv4/ IPv6 address
        or the DNS name
        Must not contain the protocol definition, this has to be set
        via the protocol attribute
    :attribute: protocol: defines the protocol (http/https) for connecting to the PLC
    :attribute: verifyTls: Switch wether TLS Server Certificate should be verified against
        trusted certificates or trusted by default
    """
    address = ""
    protocol = ""
    verifyTls = True


class JsonrpcBaseRequest():
    r"""Represents a base type for all jsonrpc requests against
    the SIMATC S7 webserver
    Provides all functions to build the request and execute it.

    :attribute: method: defines the jsonrpc method and functions that are
        defined for the WebAPI
    :attribute: params: defines additional parameters required by the specific request methods
    :attribute: address: Address of the PLC webserver, can be either a IPv4/ IPv6 address
        or the DNS name
        Must not contain the protocol definition, this has to be set
        via the protocol attribute
    :attribute: protocol: defines the protocol (http/https) for connecting to the PLC
    :attribute: token: Token for authentication and authorization on the PLC
    :attribute: verifyTls: Switch wether TLS Server Certificate should be verified against
        trusted certificates or trusted by default
    """
    method = None
    params = None
    address = ""
    protocol = ""
    token = None
    verifyTls = True
    response: requests.Response | None = None

    def headers(self):
        r"""Creates an object for the necessary header fields
        """

        if self.token:
            return {"Content-type": "application/json",
                    "X-Auth-Token": self.token}
        return {"Content-type": "application/json"}

    def body(self):
        r"""Creates the body object of the request
        """

        req_body = {
            "id": random.randint(1, 1000),
            "jsonrpc": "2.0",
            "method": self.method
        }
        if self.params:
            req_body["params"] = self.params

        return req_body

    def url(self):
        r"""Creates the url based on the information address and protocol
        """
        return f"{self.protocol}://{self.address}/api/jsonrpc"

    def __str__(self):
        return f"""---HTTP POST Request to {self.url()}---
        \tHeaders: {self.headers()}
        \tBody: {self.body()}"""

    def request(self) -> requests.Response:
        r"""Executes the POST request against the webserver

        :return: :class:`Response <Response>` object
        :rtype: requests.Response

        Raises
        ------
        requests.RequestException
            There was an ambiguous that occurred while handling your request.

        requests.ConnectionError
            A Connection error occurred.

        requests.HTTPError
            An HTTP error occurred.

        requests.URLRequired
            A valid URL is required to make a request.

        requests.TooManyRedirects
            Too many redirects.

        requests.ConnectTimeout
            The request timed out while trying to connect to the remote server.

            Requests that produced this error are safe to retry.

        requests.ReadTimeout
            The server did not send any data in the allotted amount of time.

        requests.Timeout
            The request timed out.

            Catching this error will catch both
            ConnectTimeout and ReadTimeout errors.

        requests.JSONDecodeError
            Couldn’t decode the text into json
        """
        self.response = requests.post(self.url(), json=self.body(),
                                      headers=self.headers(), verify=self.verifyTls)
        return self.response

    def execute(self):
        post_res = self.request()
        logger = logging.getLogger("stdout")
        logger.debug(self.__str__())
        logger.debug(self.format_response())
        # logger.debug(post_res.json())

        if post_res is None:
            logger.error("Response was empty, unable to parse")
            return None

        res = JsonrpcBaseResponse.parse(post_res)

        if res is None:
            logger.error("Unable to parse the response, it is not in typical jsonrpc format")
            return None
        if res.is_error():
            logger.error(f"WebAPI responded with an error: {res.error.__str__()}")
            return None

        return self.parse(res)

    def __new__(cls, config: RequestConfig, *args, **kwargs):

        self = super().__new__(cls)

        self.verifyTls = config.verifyTls
        self.address = config.address
        self.protocol = config.protocol
        self.token = None

        self.__init__(config, *args, **kwargs)

        if self.method is None:
            raise UnboundLocalError("Method name must be assigned")

        return self

    def format_response(self):
        if self.response is None:
            return None
        current_time = datetime.now().time()
        return f"""---HTTP POST Request---{current_time}
        \tResponse code: {self.response.status_code}
        \tResponse: {self.response.json()}"""

    def parse(self, response: JsonrpcBaseResponse) -> str | None:
        r"""
        Parses the response of a simple request and returns the
        result as a string.
        If no result string is provided or the request failed None is returned.
        only works for {.. result: "somestring" ..}

        :param: response: The :class:`JsonrpcBaseResponse <JsonrpcBaseResponse>`
        """
        logger = logging.getLogger("stdout")
        if response.is_error():
            logger.debug("Response has error")
            return None
        if response.result is None:
            logger.debug("Response result structure is None")
            return None

        return str(response.result)
