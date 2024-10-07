import requests


class JsonrpcError:
    r"""Base type for all errors returned by the SIMATIC S7 Webserver

    :attribute: code: Code of the error, defined in webserver documentation
    :attribute: message: Optional additional information provided by the Webserver
    :attribute: http_code: HTTP Response code provided by the server response
    """
    code: int
    message: str | None
    http_code: int

    def __init__(self, http_code: int, code: int = -1, message: str | None = None):
        r"""Constructor for the error type

        :param: http_code: HTTP Response code provided by the server response
        :param: code: Optional code of the error, defined in webserver documentation
        :param: message: Optional additional information provided by the Webserver
        """
        self.http_code = http_code
        self.code = code
        self.message = message

    def __str__(self) -> str:
        r"""String formatter for the error type
        """
        if self.message:
            return f"HTTP {self.http_code} - [{self.code}]: {self.message}"
        return f"HTTP {self.http_code} - [{self.code}]: No message, further information provided in the docs"


class JsonrpcBaseResponse:
    r"""Base type for all responsed returned by the SIMATIC S7 Webserver

    :attribute: error: Generic type for error if there is one, else None
    :attribute: result: Object that provides result data
    :attribute: raw: Generic HTTP response
    """
    error: JsonrpcError | None
    result: None
    raw: requests.Response

    def __init__(self) -> None:
        self.error = None
        self.result: None

    def is_error(self) -> bool:
        return self.error is not None or self.result is None

    @staticmethod
    def parse(response: requests.Response):
        r"""Tries to parse a generic HTTP response into the specific jsonrpc
        response format. Returns None if parsing is not successfull

        :param: response: Generic HTTP response
        """

        res = JsonrpcBaseResponse()
        if int(response.status_code) != 200:
            res.error = JsonrpcError(response.status_code)
            return res

        json_response = response.json()

        if "result" in json_response:
            res.result = json_response["result"]
            return res
        if "error" in json_response:
            msg = None
            code = -1
            if "message" in json_response["error"]:
                msg = json_response["error"]["message"]
            if "code" in json_response["error"]:
                code = json_response["error"]["code"]

            res.error = JsonrpcError(response.status_code, code=code, message=msg)
            return res

        return None

    def __str__(self) -> str:
        if self.is_error():
            return f"Error response: {self.error.__str__()}"
        return f"Good response: {self.result}"
