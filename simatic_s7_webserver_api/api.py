from enum import Enum
import logging
from typing import List
import simatic_s7_webserver_api.request
from simatic_s7_webserver_api.response import JsonrpcBaseResponse
from simatic_s7_webserver_api.util import get_array_named_values


class ApiTicketState(Enum):
    CREATED = 'created'
    ACTIVE = 'active'
    COMPLETED = 'completed'
    FAILED = 'failed'


class ApiTicket:
    r"""
    :attribute: id: Ticket ID.
    :attribute: date_created: ISO8601 time stamp as a string. Time of the ticket creation based on CPU time.
    :attribute: provider: Name of the method that has created the ticket.
    :attribute: state: Current ticket status. It could be: 'created', 'active', 'completed' or 'failed'
    :attribute: data: additional ticket data. Some methods include additional information to the user.
    """
    id: str
    date_created: str
    provider: str
    state: ApiTicketState
    data = None


class CustomTicket:
    r"""
    :attribute: max_tickets: maximum number of tickets for one session.
    :attribute: ticket: The :class:`ApiTicket <ApiTicket>`
    """

    max_tickets: int
    ticket: ApiTicket


class ApiLogin(simatic_s7_webserver_api.request.JsonrpcBaseRequest):
    method = "Api.Login"

    def __init__(self, config: simatic_s7_webserver_api.request.RequestConfig, user: str = "Anonymous", password: str = ""):
        r"""Constructor that allows the user to login

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: user: the user name.
        :param: password: the current password.
        """
        self.params = {"user": user, "password": password}

    def parse(self, response: JsonrpcBaseResponse) -> str | None:
        r"""
        Parses the response of a login request and returns the user token.
        If no user token is found our the request failed None is returned.

        :param: response: The :class:`JsonrpcBaseResponse <JsonrpcBaseResponse>` returned by the post
        :response: The token that indicates that its holder has successfully authenticated themselves at the WebAPI.
        """
        if response.is_error() or response.result is None:
            return None

        if "token" in response.result:
            return response.result["token"]

        return None


class ApiLogout(simatic_s7_webserver_api.request.JsonrpcBaseRequest):
    method = "Api.Logout"

    def __init__(self, config: simatic_s7_webserver_api.request.RequestConfig, token):
        r"""Constructor to logout from the Web API session

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        """
        self.token = token
        r"""
    :response: If succesful, the server returns the Boolean value 'True'"""


class ApiPing(simatic_s7_webserver_api.request.JsonrpcBaseRequest):
    method = "Api.Ping"
    r"""
    :response: The system outputs a unique ID for the CPU used, teh CPU ID comprises a 28-byte string. """


class ApiBrowse(simatic_s7_webserver_api.request.JsonrpcBaseRequest):
    method = "Api.Browse"

    def parse(self, response: JsonrpcBaseResponse) -> List[str] | None:
        r"""
        Parses the response of a browse request and returns the individual method strings.
        If no method is provided or the request failed None is returned.

        :param: response: The :class:`JsonrpcBaseResponse <JsonrpcBaseResponse>`
        :response: A list of all methods that you can call via the Web API with the current firmware.
        """
        if response.is_error():
            return None
        return get_array_named_values(response)


class ApiGetPermissions(simatic_s7_webserver_api.request.JsonrpcBaseRequest):
    method = "Api.GetPermissions"

    def __init__(self, config: simatic_s7_webserver_api.request.RequestConfig, token):
        r"""Constructor to know  actions that the user is authorized to do.

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        """
        self.token = token

    def parse(self, response: JsonrpcBaseResponse) -> List[str] | None:
        r"""
        Parses the response of a get permissions request and returns the individual permissions as strings.
        If no permission is provided or the request failed None is returned.

        :param: response: The :class:`JsonrpcBaseResponse <JsonrpcBaseResponse>`
        :response: A list of actions for whose execution the user is authorized.
        """
        if response.is_error():
            return None

        return get_array_named_values(response)


class ApiVersion(simatic_s7_webserver_api.request.JsonrpcBaseRequest):
    method = "Api.Version"

    r"""
    Returns the current version number of the Web API"""


class ApiGetCertificateUrl(simatic_s7_webserver_api.request.JsonrpcBaseRequest):
    method = "Api.GetCertificateUrl"

    r"""
    The method outputs a string with a relative URL to the root directory of the CPU Web server (https://[ip-address]).
    If the Web server has not been configured with a CA certificate generated via the global security settings, the method outputs an empty string.
    """


class ApiBrowseTickets(simatic_s7_webserver_api.request.JsonrpcBaseRequest):
    method = "Api.BrowseTickets"

    def __init__(self, config: simatic_s7_webserver_api.request.RequestConfig, token: str, id: str | None = None):
        r"""Constructor to know all the tickets of a logged-in user

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: id: the ticket ID that was returned by an API method for use by the ticket system. If no parameter is specified, then the response is componend by all the tickets of the user.
        """
        self.token = token
        if id is None:
            return
        self.params = {"id": id}

    def parse(self, response: JsonrpcBaseResponse) -> CustomTicket | None:
        r"""
        Parses the response of a get permissions request and returns a custom object..
        If no permission is provided or the request failed None is returned.

        :param: response: The :class:`JsonrpcBaseResponse <JsonrpcBaseResponse>`
        :response: CustomTicket: The :class:`CustomTicket <CustomTicket>`
        """
        logger = logging.getLogger("stdout")
        if response.is_error() or response.result is None:
            logger.error("Response has error or response result does not exist")
            return None

        if "tickets" not in response.result or response.result["tickets"] is None:
            logger.error("Tickets object not found in response or tickets are empty")
            return None

        if len(response.result["tickets"]) <= 0:
            logger.error("Tickets array is empty")
            return None

        customTicket = CustomTicket()
        customTicket.ticket = list[ApiTicket]()

        if "max_tickets" in response.result:
            customTicket.max_tickets = response.result["max_tickets"]
            for ticket in response.result["tickets"]:
                _temp = ApiTicket()

            if "id" in ticket:
                _temp.id = ticket["id"]
            if "state" in ticket:
                _temp.state = ticket["state"]
            if "povider" in ticket:
                _temp = ticket["provider"]
            if "date_created" in ticket:
                _temp.date_created = ticket["date_created"]
            if "data" in ticket:
                _temp.data = ticket["data"]

            customTicket.ticket.append(_temp)
            # print(*ticket)
        return customTicket


class ApiCloseTicket(simatic_s7_webserver_api.request.JsonrpcBaseRequest):
    method = "Api.CloseTicket"

    def __init__(self, config: simatic_s7_webserver_api.request.RequestConfig, token: str, id: str):
        r"""
        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: id: the ticket ID returned by an API method for use by the ticket system.
        """
        self.token = token
        self.params = {"id": id}

    r"""
    :response: If succesful, the server returns the Boolean value 'True'"""
