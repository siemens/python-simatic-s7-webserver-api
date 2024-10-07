from typing import List
from simatic_s7_webserver_api.response import JsonrpcBaseResponse


def get_array_named_values(response: JsonrpcBaseResponse) -> List[str] | None:
    r"""Function used to manage a response and extract what is inside of each "name" index.

        :param: response: The :class:`JsonrpcBaseResponse <JsonrpcBaseResponse>`
    """
    values = []
    if response.is_error() or response.result is None:
        return None
    try:
        for value in iter(response.result):
            if "name" in value:
                values.append(value["name"])
    except Exception:
        return None

    if values is None or len(values) == 0:
        return None

    return values
