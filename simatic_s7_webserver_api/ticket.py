import logging
import requests
from simatic_s7_webserver_api.request import JsonrpcBaseRequest, RequestConfig


class TicketDownloadData(JsonrpcBaseRequest):
    method = "NotUsed"

    def __init__(self, config: RequestConfig, ticket_id: str, token: str | None = None):
        r""" Constructor used to download data from the CPU

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: ticket_id: ticket ID generated in a method that needs to work with the ticket management system.
        :param: token: The user token that identifies the user as successfully authenticated with its permissions."""

        self.params = ticket_id
        self.token = token

    def body(self):
        r"""Overwrites the body method of base request.
        No body is needed for ticket requests
        """
        return ""

    def url(self):
        r"""Creates the url based on the information address and protocol
        Differs from base JSONRPC request in the route params"""
        id = self.params
        return f"{self.protocol}://{self.address}/api/ticket?id={id}"

    def request(self) -> requests.Response:
        return requests.get(self.url(), headers=self.headers(), verify=self.verifyTls)

    def execute(self):
        get_res = self.request()
        logger = logging.getLogger("stdout")
        logger.debug(self.__str__())
        logger.debug(self.format_response)

        if get_res is None:
            logger.error("Response was empty, unable to parse")
            return None

        if int(get_res.status_code) != 200:
            logger.error(f"Failed to retrieve data from ticket {self.params}, request returned response code {get_res.status_code}")
            return None

        return get_res.content


class TicketUploadData(TicketDownloadData):
    method = "NotUsed"
    data = bytes()

    def __init__(self, config: RequestConfig, ticket_id: str, data: bytes, token: str | None = None):
        r""" Constructor used to upload data to the CPU

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: ticket_id: ticket ID generated in a method that needs to work with the ticket management system.
        :param: data: data that is going to be uploaded. It must be in bytes format.
        :param: token: The user token that identifies the user as successfully authenticated with its permissions."""

        self.params = ticket_id
        self.token = token
        self.data = data

    def headers(self):
        if self.token:
            return {"Content-Type": "application/octet-stream", "X-Auth-Token": self.token}
        return {"Content-Type": "application/octet-stream"}

    def request(self) -> requests.Response:
        return requests.post(self.url(), headers=self.headers(), verify=self.verifyTls, data=self.data)

    def execute(self):
        get_res = self.request()
        logger = logging.getLogger("stdout")
        logger.debug(self.__str__())
        logger.debug(self.format_response)

        if get_res is None:
            logger.error("Response was empty, unable to parse")
            return None

        if int(get_res.status_code) != 200:
            logger.error(f"Failed to upload data for ticket {self.params}, request returned response code {get_res.status_code}")
            return None

        return get_res.status_code
