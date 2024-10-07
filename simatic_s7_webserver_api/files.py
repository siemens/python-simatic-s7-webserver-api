from datetime import datetime
from simatic_s7_webserver_api.request import JsonrpcBaseRequest, RequestConfig
from simatic_s7_webserver_api.response import JsonrpcBaseResponse


class FilesBrowseEntry:
    r"""
    :attribute: name: name of the entry.
    :attribute: type: type of the entry, either 'file' or 'dir'.
    :attribute: size: size of the file in bytes (if type is 'file').
    :attribute: last_modified: The ISO8601 time stamp as a string, contains the time of the last change.
    :attribute: state: reserved for active or inactive DataLogs in the 'DataLogs' folder."""

    name: str
    type: str
    size: int | None
    last_modified: datetime
    state: str | None


class FilesBaseRequest(JsonrpcBaseRequest):
    def __init__(self, config: RequestConfig, token: str, resource: str) -> None:
        r"""Constructor used in all these methods related with Files: browse, download, create, delete and create directory

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: resource: Path to the directory or file from the root node. For the root node, the use of a '/' is necessary.
        """

        self.params = {"resource": resource}
        self.token = token


class FilesBrowse(FilesBaseRequest):
    method = "Files.Browse"

    def parse(self, response: JsonrpcBaseResponse) -> list[FilesBrowseEntry] | None:
        r"""
        Parses the response of a browse files request and returns a list of files with its attributes.

        :param: response: The :class:`JsonrpcBaseResponse <JsonrpcBaseResponse>`
        :response: list compound of files from The :class:`FilesBrowseEntry <FilesBrowseEntry>` """

        if response.is_error():
            return None
        if not hasattr(response.result, '__iter__'):
            return None

        filesBrowse = list[FilesBrowseEntry]()
        for files_raw in response.result["resource"]:
            files_temp = FilesBrowseEntry()
            if "name" in files_raw:
                files_temp.name = files_raw["name"]
            if "type" in files_raw:
                files_temp.type = files_raw["type"]
            if "size" in files_raw:
                files_temp.size = files_raw["size"]
            if "last_modified" in files_raw:
                files_temp.last_modified = files_raw["last_modified"]
            if "state" in files_raw:
                files_temp.state = files_raw["state"]

            filesBrowse.append(files_temp)
        return filesBrowse


class FilesDownload(FilesBaseRequest):
    method = "Files.Download"
    r"""
    :response: This method returns a character string that includes a valid ticket ID."""


class FilesCreate(FilesBaseRequest):
    method = "Files.Create"
    r"""
    :response: This method returns a character string that includes a valid ticket ID."""


class FilesRename(JsonrpcBaseRequest):
    method = "Files.Rename"

    def __init__(self, config: RequestConfig, token: str, resource: str, new_resource: str) -> None:
        r"""Constructor used to change the name of a file or a directory. It can be used also to move files from one directory to another

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: resource: current  file path or directory path.
        :param: new_resource: new file path or directory path.
        """
        self.params = {"resource":  resource, "new_resource": new_resource}
        self.token = token
    r"""
    :response: If succesful, the server returns the Boolean value 'True'"""


class FilesDelete(FilesBaseRequest):
    method = "Files.Delete"
    r"""
    :response: If succesful, the server returns the Boolean value 'True'"""


class FilesCreateDirectory(FilesBaseRequest):
    method = "Files.CreateDirectory"
    r"""
    :response: If succesful, the server returns the Boolean value 'True'"""


class FilesDeleteDirectory(FilesBaseRequest):
    method = "Files.DeleteDirectory"
    r"""
    :response: If succesful, the server returns the Boolean value 'True'"""
