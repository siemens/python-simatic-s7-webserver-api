from simatic_s7_webserver_api.request import JsonrpcBaseRequest, RequestConfig


class DataLogsDownloadAndClear(JsonrpcBaseRequest):
    method = "DataLogs.DownloadAndClear"

    def __init__(self, config: RequestConfig, token: str, resource: str) -> None:
        r"""
        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: resource: The name of the DataLog you want to download. Alternatively, the user can use a path starting with /datalogs/
        """
        self.params = {"resource": resource}
        self.token = token
    r"""
    :response: This method returns a character string that includes a valid ticket ID."""
