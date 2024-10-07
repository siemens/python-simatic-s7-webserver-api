import datetime
from enum import Enum
from simatic_s7_webserver_api.request import JsonrpcBaseRequest, RequestConfig
from simatic_s7_webserver_api.response import JsonrpcBaseResponse


class PlcOperatingMode(Enum):
    STOP = "stop"
    STARTUP = "startup"
    RUN = "run"
    HOLD = "hold"
    UNKNOWN = ""


class PlcReadOperatingMode(JsonrpcBaseRequest):
    method = "Plc.ReadOperatingMode"

    def __init__(self, config: RequestConfig, token: str):
        r"""Constructor used to read the operating mode of the PLC

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions."""

        self.token = token

    def parse(self, response: JsonrpcBaseResponse) -> PlcOperatingMode | None:
        r"""
        Parses the response of a plc read operating mode request and returns the current status.

        :param: response: The :class:`JsonrpcBaseResponse <JsonrpcBaseResponse>`
        :response: PlcOperatingMode: The class :class:`PlcOperatingMode <PlcOperatingMode>` """

        if response.is_error() or response.result is None:
            return None
        try:
            return getattr(PlcOperatingMode, str(response.result).upper())
        except Exception:
            return None


class PlcRequestChangeOperatingMode(JsonrpcBaseRequest):
    method = "Plc.RequestChangeOperatingMode"

    def __init__(self, config: RequestConfig, token: str, mode: PlcOperatingMode):
        r"""Constructor used to request to change the operating mode of the PLC

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: mode: The :class:`PlcOperatingMode <PlcOperatingMode>`
        """

        if mode == PlcOperatingMode.STARTUP or mode == PlcOperatingMode.HOLD:
            raise Exception("Mode for mode change my only be Start or Stop")
        self.params = {"mode": mode.value}
        self.token = token

    def parse(self, response: JsonrpcBaseResponse) -> bool:
        r"""
        Parses the response of a plc change operating mode request and returns a boolean if the change is satisfied.

        :param: response: The :class:`JsonrpcBaseResponse <JsonrpcBaseResponse>`
        :response: Boolean with 'True' value."""

        if response.is_error() or response.result is None:
            return False
        return bool(response.result)


class PlcCreateBackup(JsonrpcBaseRequest):
    method = "Plc.CreateBackup"

    def __init__(self, config: RequestConfig, token: str):
        r"""Constructor used to request a ticket to create a backup file of the CPU configuration

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions."""
        self.token = token
    r"""
    :response: This method returns a character string that includes a valid ticket ID."""


class PlcRestoreBackup(JsonrpcBaseRequest):
    method = "Plc.RestoreBackup"

    def __init__(self, config: RequestConfig, token: str, password: str):
        r"""Constructor used to request a ticket to restore the configuration of a CPU using a backup file.

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: password: the required password for the logged on user, this password must be the same of the user authenticated previously with via the Api.Login method.
        """
        self.token = token
        self.params = {"password": password}


class PlcReadSystemTime(JsonrpcBaseRequest):
    method = "Plc.ReadSystemTime"

    def parse(self, response: JsonrpcBaseResponse) -> datetime.datetime | None:
        r"""
        Parses the response of a plc read system time request and returns the time stamp, if the user synchronized the system time of the CPU,  the time corressponds to the Coordinated Universal Time (UCT).

        :param: response: The :class:`JsonrpcBaseResponse <JsonrpcBaseResponse>`
        :response: datetime: timestamp with USO8601 format as a string."""

        if response.result is None or "timestamp" not in response.result:
            return None
        timestampstr = str(response.result["timestamp"]).split(".")
        timestamp = datetime.datetime.strptime(timestampstr[0], "%Y-%m-%dT%H:%M:%S")
        ms = 1 / float(timestampstr[1].replace("Z", "")) * 1000
        return timestamp + datetime.timedelta(milliseconds=ms)


class PlcReadTimeSettings(JsonrpcBaseRequest):
    method = "Plc.ReadTimeSettings"

    r"""
    :response: returns the current active time, the deviation of the time zone from the UCT and any daylight saving time rules."""

# FOR NEXT VERSION
# class RuleStart:
#     month: int
#     week: int
#     day_of_week: str
#     hour: int
#     minute: int

# class RuleStd:
#     ruleStart: RuleStart

#     ruleStart = RuleStart()

# class RuleDst:
#     ruleStart : RuleStart
#     offset: str

#     ruleStart = RuleStart()
# class Rule:
#     ruleStd: RuleStd
#     ruleDst: RuleDst

#     ruleStd = RuleStd()
#     ruleDst = RuleDst()


# class TimeSettings:
#     current_offset: str
#     utc_offset: str
#     rule: Rule | None

#     rule = Rule()


# class PlcSetTimeSettings(JsonrpcBaseRequest):
#     method = "Plc.SetTimeSettings"

#     def __init__(self, config: RequestConfig, TimeSettings: TimeSettings):
#         if TimeSettings.rule is None:
#             self.params = {"current_offset": TimeSettings.current_offset, "utc_offset": TimeSettings.utc_offset}
#             return
#         else:
#             """elif TimeSettings.rule.ruleStd is None:          #If is not a Std Rule, I suposse that is a DST Rule
#                 self.params = {"current_offset": TimeSettings.current_offset, "utc_offset": TimeSettings.utc_offset, "rule.dst.offset": TimeSettings.rule.ruleDst.offset, "rule.dst.start.month": TimeSettings.rule.ruleDst.ruleStart.month,"rule.dst.start.week": TimeSettings.rule.ruleDst.ruleStart.week, \
#                                 "rule.dst.start.day_of_week":TimeSettings.rule.ruleDst.ruleStart.day_of_week,"rule.dst.start.hour": TimeSettings.rule.ruleDst.ruleStart.hour,"rule.dst.start.minute": TimeSettings.rule.ruleDst.ruleStart.minute}
#                 elif TimeSettings.rule.ruleDst is None:          #If is not a Dst Rule, I suposse that is a STD Rule
#                 self.params = {"current_offset": TimeSettings.current_offset, "utc_offset": TimeSettings.utc_offset, "rule.std.start.month": TimeSettings.rule.ruleStd.ruleStart.month,"rule.std.start.week": TimeSettings.rule.ruleStd.ruleStart.week, \
#                                 "rule.std.start.day_of_week":TimeSettings.rule.ruleStd.ruleStart.day_of_week,"rule.std.start.hour": TimeSettings.rule.ruleStd.ruleStart.hour,"rule.std.start.minute": TimeSettings.rule.ruleStd.ruleStart.minute} """
#
#             self.params = {"current_offset": TimeSettings.current_offset, "utc_offset": TimeSettings.utc_offset, "rule.dst.offset": TimeSettings.rule.ruleDst.offset, "rule.dst.start.month": TimeSettings.rule.ruleDst.ruleStart.month,"rule.dst.start.week": TimeSettings.rule.ruleDst.ruleStart.week, \
#                             "rule.dst.start.day_of_week":TimeSettings.rule.ruleDst.ruleStart.day_of_week,"rule.dst.start.hour": TimeSettings.rule.ruleDst.ruleStart.hour,"rule.dst.start.minute": TimeSettings.rule.ruleDst.ruleStart.minute, \
#                             "rule.std.start.month": TimeSettings.rule.ruleStd.ruleStart.month,"rule.std.start.week": TimeSettings.rule.ruleStd.ruleStart.week, \
#                             "rule.std.start.day_of_week":TimeSettings.rule.ruleStd.ruleStart.day_of_week,"rule.std.start.hour": TimeSettings.rule.ruleStd.ruleStart.hour,"rule.std.start.minute": TimeSettings.rule.ruleStd.ruleStart.minute}
