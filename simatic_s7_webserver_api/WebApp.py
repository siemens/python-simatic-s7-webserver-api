import simatic_s7_webserver_api.request as request
import simatic_s7_webserver_api.response as response


class WebAppApplication:
    r"""
    :attribute: name: name of the application.
    :attribute: state: the status of the application, could be disabled (not reachable via HTTP point) or enbled (reachable via HTTP point).
    :attribute: type: type of the application, user (created by the user).
    :attribute: default_page: default page when no resource name was specified when accessing in the web application.
    :attribute: not_found_page: substitute page in an application when the requested resource is not found.
    :attribute: not_authorized_page: if the user tries to access a protected resource when it does not have access."""

    name: str
    state: str
    type: str
    default_page: str | None
    not_found_page: str | None
    not_authorized_page: str | None


class CustomWebAppBrowse:
    r"""
    :attribute: max_applications: number of maximum applications supported by the CPU.
    :attribute: applications: list of strings with the individual application parameters: name, state and type. Optinal also default page, not found page and not authorized page."""

    max_applications: int
    applications: WebAppApplication


class WebAppBrowse(request.JsonrpcBaseRequest):
    method = "WebApp.Browse"

    def __init__(self, config: request.RequestConfig,  name: str | None):
        r"""Constructor to browse web applications

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: name: Name of a web application. If this parameter does not exist, all applications will be returned by the method. If the parameter is available, the list will contain only the application whose name matches this parameter. """

        if name is None:
            return
        self.params = {"name": name}

    def parse(self, response: response.JsonrpcBaseResponse) -> CustomWebAppBrowse | None:
        r"""
        Parses the response of a browse web applications request and returns a custom object.

        If no method is provided or the request failed None is returned.

        :param: response: The :class:`JsonrpcBaseResponse <JsonrpcBaseResponse>`
        :response: CustomWebAppBrowse: The :class:`CustomWebAppBrowse <CustomWebAppBrowse>`
        """

        if response.is_error():
            return None

        if not hasattr(response.result, '__iter__'):
            return None

        customWebAppBrowse = CustomWebAppBrowse()
        customWebAppBrowse.applications = list[WebAppApplication]()

        if "max_applications" in response.result:
            customWebAppBrowse.max_applications = (f"max_applications  :  {str(response.result['max_applications'])}")

        for app_raw in response.result["applications"]:
            app_temp = WebAppApplication()

            if "name" in app_raw:
                app_temp.name = app_raw["name"]
            if "state" in app_raw:
                app_temp.state = app_raw["state"]
            if "type" in app_raw:
                app_temp.type = app_raw["type"]
            if "default_page" in app_raw:
                app_temp.default_page = app_raw["default_page"]
            if "not_found_page" in app_raw:
                app_temp.not_found_page = app_raw["not_found_page"]
            if "not_authorized_page" in app_raw:
                app_temp.not_authorized_page = app_raw["not_authorized_page"]

            customWebAppBrowse.applications.append(app_temp)

            return customWebAppBrowse


class WebAppResource:
    r""""
    :attribute: name: name of the resource.
    :attribute: syze: size of the resource in bytes.
    :attribute: media_type: media type of the resource.
    :attribute: ETag: ETag value of the resource.
    :attribute: visibility: visibility of the resource.
    :attribute: last_modified: ISO8601 time stamp as a string. The time stamp of the last modification.
    """
    name: str
    size: int
    media_type: str
    etag: str | None
    visibility: str
    last_modified: str


class CustomWebAppResources:
    r"""
    :attribute: max_resources: number of maximum resources supported by the CPU.
    :attribute: resources: list of strings with the individual resources parameters: name, size, media type, visibility and last modified. Optional can also contain the ETAG value of the resource."""

    max_resources: int
    resources: WebAppResource


class WebAppBrowseResources(request.JsonrpcBaseRequest):
    method = "WebApp.BrowseResources"

    def __init__(self, config: request.RequestConfig, token: str, app_name: str, name: str | None = None):
        r"""Constructor for browsing resources on a custom web app

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: app_name: The name of the web application whose list is provided.
        :param: name: If this parameter does not exist, all resources must be returned. Otherwise, the list of returned resources only contains one resource whose name matches this parameter.
                If no such resource is found, then: The return list must be empty and it is not an error. """

        self.token = token
        if name is None:
            self.params = {"app_name": app_name}
        else:
            self.params = {"app_name": app_name, "name": name}

    def parse(self, response: response.JsonrpcBaseResponse) -> CustomWebAppResources | None:
        r"""
        Parses the response of a browse resources request and returns a custom object.

        :param: response: The :class:`JsonrpcBaseResponse <JsonrpcBaseResponse>`
        :response: CustomWebAppResources: The :class:`CustomWebAppResources <CustomWebAppResources>` """

        if response.is_error():
            return None
        if not hasattr(response.result, '__iter__'):
            return None

        customWebAppResource = CustomWebAppResources()
        customWebAppResource.resources = list[WebAppResource]()

        if "max_resources" in response.result:
            customWebAppResource.max_resources = (f"max_resources :  {response.result['max_resources']}")
        for resource_raw in response.result["resources"]:
            resource_temp = WebAppResource()
            if "name" in resource_raw:
                resource_temp.name = resource_raw["name"]
            if "size" in resource_raw:
                resource_temp.size = resource_raw["size"]
            if "media_type" in resource_raw:
                resource_temp.media_type = resource_raw["media_type"]
            if "etag" in resource_raw:
                resource_temp.etag = resource_raw["etag"]
            if "visibility" in resource_raw:
                resource_temp.visibility = resource_raw["visibility"]
            if "last_modified" in resource_raw:
                resource_temp.last_modified = resource_raw["last_modified"]

            customWebAppResource.resources.append(resource_temp)

        return customWebAppResource


class WebAppCreate(request.JsonrpcBaseRequest):
    method = "WebApp.Create"

    def __init__(self, config: request.RequestConfig, token: str, name: str, state: str = "enabled"):
        r"""Constructor to create new web applications in the CPU

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: name: name of the user-defined web application.
        :param: state: "disabled" if pages cannot be reached via HTTP end point or "enabled" if pages can be reached via HTTP end point (default value)."""

        self.token = token
        self.params = {"name": name, "state": state}
    r"""
    :response: If succesful, the server returns the Boolean value 'True'"""


class WebAppCreateResource(request.JsonrpcBaseRequest):
    method = "WebApp.CreateResource"

    def __init__(self, config: request.RequestConfig, token: str, app_name: str, name: str, media_type: str, last_modified: str, visibility: str = "public", etag: str = ""):
        r"""Constructor to create a new resource in a web application that was loaded by the user

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: app_name: The name of the web application for which the resource must be created.
        :param: name: name of the resource that is uploaded.
        :param: media_type: media type of the resource.
        :param: last_modified: the time stamp of the last modification (ISO8601 type).
        :param: visibility: visibility of the resoruce. "public" by default.
        :param: etag: ETAG value of the resource. Default empty string (OPTIONAL). """

        self.token = token
        self.params = {"app_name": app_name, "name": name, "media_type": media_type, "visibility": visibility, "etag": etag, "last_modified": last_modified}

    r"""
    :response: This method returns a character string that includes a valid ticket ID."""


class WebAppDelete(request.JsonrpcBaseRequest):
    method = "WebApp.Delete"

    def __init__(self, config: request.RequestConfig, token: str, name: str):
        r"""Constructor for delete an existing web application and its resources

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: app_name: The name of the web application that is deleted."""

        self.token = token
        self.params = {"name": name}
    r"""
    :response: If succesful, the server returns the Boolean value 'True'"""


class WebAppDeleteResource(request.JsonrpcBaseRequest):
    method = "WebApp.DeleteResource"

    def __init__(self, config: request.RequestConfig, token: str, app_name: str, name: str):
        r"""Constructor for delete resource from a specific web application

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: app_name: The name of the web application for which the resource must be deleted.
        :param: name: name of the resource that is deleted. """

        self.token = token
        self.params = {"app_name": app_name, "name": name}

    r"""
    :response: If succesful, the server returns the Boolean value 'True'"""


class WebAppDownloadResource(request.JsonrpcBaseRequest):
    method = "WebApp.DownloadResource"

    def __init__(self, config: request.RequestConfig, token: str, app_name: str, name: str):
        r"""Constructor for download a resource from a web application

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: app_name: The name of the web application that contains the resource.
        :param: name: name of the resource that is downloaded. """

        self.token = token
        self.params = {"app_name": app_name, "name": name}

    r"""
    :response: This method returns a character string that includes a valid ticket ID."""


class WebAppRename(request.JsonrpcBaseRequest):
    method = "WebApp.Rename"

    def __init__(self, config: request.RequestConfig, token: str, name: str, new_name: str):
        r"""Constructor that allows you to change the name of a web application

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: name: The current name of the web application.
        :param: new_name: The new name of the web application."""

        self.token = token
        self.params = {"name": name, "new_name": new_name}

    r"""
    :response: If succesful, the server returns the Boolean value 'True'"""


class WebAppRenameResource(request.JsonrpcBaseRequest):
    method = "WebApp.RenameResource"

    def __init__(self, config: request.RequestConfig, token: str, app_name: str, name: str, new_name: str):
        r"""Constructor that allows you to change the name of a resource from a specific web applicaion

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: app_name: The name of the web application  that contains the resource that changes its name.
        :param: name: The current name of the resource.
        :param: new_name: The new name of the resource."""

        self.token = token
        self.params = {"app_name": app_name, "name": name, "new_name": new_name}

    r"""
    :response: If succesful, the server returns the Boolean value 'True'"""


class WebAppSetDefaultPage(request.JsonrpcBaseRequest):
    method = "WebApp.SetDefaultPage"

    def __init__(self, config: request.RequestConfig, token: str, name: str, resource_name: str):
        r"""Constructor that allows you to set a default page for an user-defined web applicaion

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: name: The name of the web application  for which the default page is to be configured.
        :param: resource_name: The resource in the web application that is going to be the default page.
        """
        self.token = token
        self.params = {"name": name, "resource_name": resource_name}

    r"""
    :response: If succesful, the server returns the Boolean value 'True'"""


class WebAppSetNotAuthorizedPage(request.JsonrpcBaseRequest):
    method = "WebApp.SetNotAuthorizedPage"

    def __init__(self, config: request.RequestConfig, token: str, name: str, resource_name: str):
        r"""Constructor for setting the publicy visible page for an user-defined web application. The page is loaded if the resource name has a protected publicity and the method allows you to access the web without a valid cookie

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: name: The name of the web application whose public page must be changed.
        :param: resource_name: The resource in the web application loaded by the user.
        """

        self.token = token
        self.params = {"name": name, "resource_name": resource_name}

    r"""
    :response: If succesful, the server returns the Boolean value 'True'"""


class WebAppSetNotFoundPage(request.JsonrpcBaseRequest):
    method = "WebApp.SetNotFoundPage"

    def __init__(self, config: request.RequestConfig, token: str, name: str, resource_name: str):
        r""" Constructor for setting a page that is loaded if in a web application you try to access to a resource that does not exist

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: name: The name of the web application that its page must be changed.
        :param: resource_name: The resource in the web application loaded by the user to be the not found page.
        """

        self.token = token
        self.params = {"name": name, "resource_name": resource_name}

    r"""
    :response: If succesful, the server returns the Boolean value 'True'"""


class WebAppSetResourceETag(request.JsonrpcBaseRequest):
    method = "WebApp.SetResourceETag"

    def __init__(self, config: request.RequestConfig, token: str, app_name: str, name: str, etag: str):
        r"""Constructor used to change or delete the ETag attribute that is returned when accessing the resource via the HTTP header
        ETag (Entity Tag) is an HTTP header field. It only serves to determine changes at the requested resource and is used to avoid redundant data transfers

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: app_name: The name of the web application that contains the resource.
        :param: name: The resource in the web application that is to be changed.
        :param: etag: The ETag value of the resource."""

        self.token = token
        self.params = {"app_name": app_name, "name": name, "etag": etag}

    r"""
    :response: If succesful, the server returns the Boolean value 'True'"""


class WebAppSetResourceMediaType(request.JsonrpcBaseRequest):
    method = "WebApp.SetResourceMediaType"

    def __init__(self, config: request.RequestConfig, token: str, app_name: str, name: str, media_type: str):
        r"""Constructor used to change the media type of a resoruce from a web application loaded by the user

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: app_name: The name of the web application that contains the resource.
        :param: name: The resource in the web application that is to be changed.
        :param: media_type: The media type of the resource.
        """

        self.token = token
        self.params = {"app_name": app_name, "name": name, "media_type": media_type}

    r"""
    :response: If succesful, the server returns the Boolean value 'True'"""


class WebAppSetResourceModificationTime(request.JsonrpcBaseRequest):
    method = "WebApp.SetResourceModificationTime"

    def __init__(self, config: request.RequestConfig, token: str, app_name: str, name: str, last_modified: str):
        r""" Constructor to set the modification time of a resource in a web application loaded by the user

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: app_name: The name of the web application that contains the resource.
        :param: name: The resource in the web application that is to be changed.
        :param: last_modified: The ISO8601 time stamp as a string, contains the time of the last change.
        """
        self.token = token
        self.params = {"app_name": app_name, "name": name, "last_modified": last_modified}

    r"""
    :response: If succesful, the server returns the Boolean value 'True'"""


class WebAppSetResourceVisibility(request.JsonrpcBaseRequest):
    method = "WebApp.SetResourceVisibility"

    def __init__(self, config: request.RequestConfig, token: str, app_name: str, name: str, visibility: str):
        r"""Constructor used to change the visibility of a resource from a web application loaded by the user

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: app_name: The name of the web application that contains the resource.
        :param: name: The resource in the web application that is to be changed.
        :param: visibility: The visibility of the resource: public or protected.
        """
        self.token = token
        self.params = {"app_name": app_name, "name": name, "visibility": visibility}

    r"""
    :response: If succesful, the server returns the Boolean value 'True'"""


class WebAppSetState(request.JsonrpcBaseRequest):
    method = "WebApp.SetState"

    def __init__(self, config: request.RequestConfig, token: str, name: str, state: str):
        r"""Constructor that allows you to activate or deactivate a web application that was loaded by the user

        :param: config: The :class:`RequestConfig <RequestConfig>`
        :param: token: The user token that identifies the user as successfully authenticated with its permissions.
        :param: name: The name of the web application that contains the resource.
        :param: state: The status of the application, could be enabled (can be reached via HTTP end point) or disabled (cannot be reached via HTTP end point)."""

        self.token = token
        self.params = {"name": name, "state": state}

    r"""
    :response: If succesful, the server returns the Boolean value 'True'"""
