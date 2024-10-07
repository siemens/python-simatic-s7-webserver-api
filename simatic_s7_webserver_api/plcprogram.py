from typing import List
import simatic_s7_webserver_api.request


class PlcProgramBrowseArrayData:
    r"""
    :attribute: start_index: Start index for this array dimension, as specified in the TIA Portal project.
    :attribute: count: Number of elements in this array dimension.
    """
    start_index: int
    count: int


class PlcProgramBrowseVariable:
    r"""
    :attribute: name: Start index for this array dimension, as specified in the TIA Portal project.
    :attribute: address: Address of the tag in STEP 7; only applicable for the tags in the ranges M, I, Q, timer and counter and tags in non-optimized data blocks.
    :attribute: read_only: Query whether the tag is read-only. The only valid value is 'True'.
    :attribute: has_children: Query whether the tag is a structured tag with child tags.
    :attribute: db_number: Numerical data block identifier. Appears when 'datatype== datablock'.
    :attribute: area: Letter which defines the range (M/I/Q/timer/counter) of the tag.
    :attribute: datatype: data type of the tag
    :attribute: max_length: If the data type is 'string' or 'wstring' this value is the maximum number of characters allowed in the tag
    :attribute: array_dimensions: Object arrays arranged from the most significant to the least significant.

    """
    name: str
    address: str | None
    read_only: bool | None
    has_children: bool | None
    db_number: int | None
    area: str | None
    datatype: str
    max_length: int | None
    array_dimensions: PlcProgramBrowseArrayData | None


class PlcProgramBrowse(simatic_s7_webserver_api.request.JsonrpcBaseRequest):
    method = "PlcProgram.Browse"

    def __init__(self, config: simatic_s7_webserver_api.request.RequestConfig, token: str, mode: str, var: str | None = None):
        r""" Constructor used to search for tags and the corresponding metadata according to the individual requirements

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: mode: determines the behavior of this method: 'var' information about the specified tag, 'children' displays information about the immediate descendants (children) of the specified tags.
        :param: type: if 'code_blocks' reads all code blocks, 'data_blocks' reads all the data blocks, 'tags' displays all tags.
        """
        if var is None:
            self.params = {"mode": mode}
        else:
            self.params = {"var": var, "mode": mode}
        self.token = token

    def parse(self, response: simatic_s7_webserver_api.request.JsonrpcBaseResponse) -> List[PlcProgramBrowseVariable] | None:
        r"""
        Parses the response of a browse tags request and returns a list of the requested vars.

        :param: response: The :class:`JsonrpcBaseResponse <JsonrpcBaseResponse>`
        :response: PlcProgramBrowseVariable: The :class:`PlcProgramBrowseVariable <PlcProgramBrowseVariable>`
        """
        if response.result is None:
            return None
        if not hasattr(response.result, '__iter__'):
            return None

        vars = list[PlcProgramBrowseVariable]()

        for var_raw in response.result:
            var = PlcProgramBrowseVariable()

            var.name = var_raw["name"] if "name" in var_raw else ""
            var.address = var_raw["address"] if "address" in var_raw else None
            var.read_only = bool(var_raw["read_only"]) if "read_only" in var_raw else None
            var.has_children = bool(var_raw["has_children"]) if "has_children" in var_raw else None
            var.db_number = int(var_raw["db_number"]) if "db_number" in var_raw else None
            var.area = var_raw["area"] if "area" in var_raw else None
            var.datatype = var_raw["datatype"] if "datatype" in var_raw else ""
            var.max_length = int(var_raw["max_length"]) if "max_length" in var_raw else None

            if "array_dimensions" in var_raw:
                var.array_dimensions = PlcProgramBrowseArrayData()
                var.array_dimensions.start_index = int(var_raw["array_dimensions"]["start_index"]) if "start_index" in var_raw["array_dimensions"] else 0
                var.array_dimensions.count = int(var_raw["array_dimensions"]["count"]) if "count" in var_raw["array_dimensions"] else 0
            vars.append(var)

        return vars


class PlcProgramRead(simatic_s7_webserver_api.request.JsonrpcBaseRequest):
    method = "PlcProgram.Read"

    def __init__(self, config: simatic_s7_webserver_api.request.RequestConfig, token: str, var: str, mode: str = "simple"):
        r"""Constructor used to read a single variable from a CPU

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: var: name of the tag to be read.
        :param: mode: determines the behavior of this method: 'simple' or 'raw' and the method will return tag values according to each name representation.
        """
        self.token = token
        self.params = {"var": var, "mode": mode}
    r"""
    :response: The server returns JSON data values"""


class PlcProgramWrite(simatic_s7_webserver_api.request.JsonrpcBaseRequest):
    method = "PlcProgram.Write"

    def __init__(self, config: simatic_s7_webserver_api.request.RequestConfig, token: str, var: str, value, mode: str = "simple"):
        r"""Constructor used to write on a single process tag to a CPU

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: var: name of the tag to be written.
        :param: value: value to be written. It depends on the operating mode.
        :param: mode: determines the format of value: 'simple' or 'raw' and the user must specify the values according to each name representation.
        """
        self.token = token
        self.params = {"var": var, "mode": mode, "value": value}
    r"""
    :response: If succesful, the server returns the Boolean value 'True'"""
