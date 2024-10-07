# simatic_s7_webserver_api package

## Submodules

## simatic_s7_webserver_api.WebApp module

### *class* simatic_s7_webserver_api.WebApp.CustomWebAppBrowse

Bases: `object`

* **Attribute:**
  max_applications: number of maximum applications supported by the CPU.
* **Attribute:**
  applications: list of strings with the individual application parameters: name, state and type. Optinal also default page, not found page and not authorized page.

#### applications *: [WebAppApplication](#simatic_s7_webserver_api.WebApp.WebAppApplication)*

#### max_applications *: int*

### *class* simatic_s7_webserver_api.WebApp.CustomWebAppResources

Bases: `object`

* **Attribute:**
  max_resources: number of maximum resources supported by the CPU.
* **Attribute:**
  resources: list of strings with the individual resources parameters: name, size, media type, visibility and last modified. Optional can also contain the ETAG value of the resource.

#### max_resources *: int*

#### resources *: [WebAppResource](#simatic_s7_webserver_api.WebApp.WebAppResource)*

### *class* simatic_s7_webserver_api.WebApp.WebAppApplication

Bases: `object`

* **Attribute:**
  name: name of the application.
* **Attribute:**
  state: the status of the application, could be disabled (not reachable via HTTP point) or enbled (reachable via HTTP point).
* **Attribute:**
  type: type of the application, user (created by the user).
* **Attribute:**
  default_page: default page when no resource name was specified when accessing in the web application.
* **Attribute:**
  not_found_page: substitute page in an application when the requested resource is not found.
* **Attribute:**
  not_authorized_page: if the user tries to access a protected resource when it does not have access.

#### default_page *: str | None*

#### name *: str*

#### not_authorized_page *: str | None*

#### not_found_page *: str | None*

#### state *: str*

#### type *: str*

### *class* simatic_s7_webserver_api.WebApp.WebAppBrowse(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), name: str | None)

Constructor to browse web applications

* **Param:**
  config: The `RequestConfig`
* **Param:**
  name: Name of a web application. If this parameter does not exist, all applications will be returned by the method. If the parameter is available, the list will contain only the application whose name matches this parameter.

#### method *= 'WebApp.Browse'*

#### parse(response: [JsonrpcBaseResponse](#simatic_s7_webserver_api.response.JsonrpcBaseResponse))

Parses the response of a browse web applications request and returns a custom object.

If no method is provided or the request failed None is returned.

* **Param:**
  response: The `JsonrpcBaseResponse`
* **Response:**
  CustomWebAppBrowse: The [`CustomWebAppBrowse`](#simatic_s7_webserver_api.WebApp.CustomWebAppBrowse)

### *class* simatic_s7_webserver_api.WebApp.WebAppBrowseResources(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, app_name: str, name: str | None = None)

Constructor for browsing resources on a custom web app

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  app_name: The name of the web application whose list is provided.
* **Param:**
  name: If this parameter does not exist, all resources must be returned. Otherwise, the list of returned resources only contains one resource whose name matches this parameter.
  If no such resource is found, then: The return list must be empty and it is not an error.

#### method *= 'WebApp.BrowseResources'*

#### parse(response: [JsonrpcBaseResponse](#simatic_s7_webserver_api.response.JsonrpcBaseResponse))

Parses the response of a browse resources request and returns a custom object.

* **Param:**
  response: The `JsonrpcBaseResponse`
* **Response:**
  CustomWebAppResources: The [`CustomWebAppResources`](#simatic_s7_webserver_api.WebApp.CustomWebAppResources)

### *class* simatic_s7_webserver_api.WebApp.WebAppCreate(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, name: str, state: str = 'enabled')

Constructor to create new web applications in the CPU

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  name: name of the user-defined web application.
* **Param:**
  state: “disabled” if pages cannot be reached via HTTP end point or “enabled” if pages can be reached via HTTP end point (default value).

#### method *= 'WebApp.Create'*

### *class* simatic_s7_webserver_api.WebApp.WebAppCreateResource(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, app_name: str, name: str, media_type: str, last_modified: str, visibility: str = 'public', etag: str = '')

Constructor to create a new resource in a web application that was loaded by the user

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  app_name: The name of the web application for which the resource must be created.
* **Param:**
  name: name of the resource that is uploaded.
* **Param:**
  media_type: media type of the resource.
* **Param:**
  last_modified: the time stamp of the last modification (ISO8601 type).
* **Param:**
  visibility: visibility of the resoruce. “public” by default.
* **Param:**
  etag: ETAG value of the resource. Default empty string (OPTIONAL).

#### method *= 'WebApp.CreateResource'*

### *class* simatic_s7_webserver_api.WebApp.WebAppDelete(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, name: str)

Constructor for delete an existing web application and its resources

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  app_name: The name of the web application that is deleted.

#### method *= 'WebApp.Delete'*

### *class* simatic_s7_webserver_api.WebApp.WebAppDeleteResource(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, app_name: str, name: str)

Constructor for delete resource from a specific web application

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  app_name: The name of the web application for which the resource must be deleted.
* **Param:**
  name: name of the resource that is deleted.

#### method *= 'WebApp.DeleteResource'*

### *class* simatic_s7_webserver_api.WebApp.WebAppDownloadResource(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, app_name: str, name: str)

Constructor for download a resource from a web application

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  app_name: The name of the web application that contains the resource.
* **Param:**
  name: name of the resource that is downloaded.

#### method *= 'WebApp.DownloadResource'*

### *class* simatic_s7_webserver_api.WebApp.WebAppRename(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, name: str, new_name: str)

Constructor that allows you to change the name of a web application

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  name: The current name of the web application.
* **Param:**
  new_name: The new name of the web application.

#### method *= 'WebApp.Rename'*

### *class* simatic_s7_webserver_api.WebApp.WebAppRenameResource(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, app_name: str, name: str, new_name: str)

Constructor that allows you to change the name of a resource from a specific web applicaion

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  app_name: The name of the web application  that contains the resource that changes its name.
* **Param:**
  name: The current name of the resource.
* **Param:**
  new_name: The new name of the resource.

#### method *= 'WebApp.RenameResource'*

### *class* simatic_s7_webserver_api.WebApp.WebAppResource

Bases: `object`

”
:attribute: name: name of the resource.
:attribute: syze: size of the resource in bytes.
:attribute: media_type: media type of the resource.
:attribute: ETag: ETag value of the resource.
:attribute: visibility: visibility of the resource.
:attribute: last_modified: ISO8601 time stamp as a string. The time stamp of the last modification.

#### etag *: str | None*

#### last_modified *: str*

#### media_type *: str*

#### name *: str*

#### size *: int*

#### visibility *: str*

### *class* simatic_s7_webserver_api.WebApp.WebAppSetDefaultPage(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, name: str, resource_name: str)

Constructor that allows you to set a default page for an user-defined web applicaion

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  name: The name of the web application  for which the default page is to be configured.
* **Param:**
  resource_name: The resource in the web application that is going to be the default page.

#### method *= 'WebApp.SetDefaultPage'*

### *class* simatic_s7_webserver_api.WebApp.WebAppSetNotAuthorizedPage(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, name: str, resource_name: str)

Constructor for setting the publicy visible page for an user-defined web application. The page is loaded if the resource name has a protected publicity and the method allows you to access the web without a valid cookie

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  name: The name of the web application whose public page must be changed.
* **Param:**
  resource_name: The resource in the web application loaded by the user.

#### method *= 'WebApp.SetNotAuthorizedPage'*

### *class* simatic_s7_webserver_api.WebApp.WebAppSetNotFoundPage(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, name: str, resource_name: str)

Constructor for setting a page that is loaded if in a web application you try to access to a resource that does not exist

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  name: The name of the web application that its page must be changed.
* **Param:**
  resource_name: The resource in the web application loaded by the user to be the not found page.

#### method *= 'WebApp.SetNotFoundPage'*

### *class* simatic_s7_webserver_api.WebApp.WebAppSetResourceETag(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, app_name: str, name: str, etag: str)

Constructor used to change or delete the ETag attribute that is returned when accessing the resource via the HTTP header
ETag (Entity Tag) is an HTTP header field. It only serves to determine changes at the requested resource and is used to avoid redundant data transfers

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  app_name: The name of the web application that contains the resource.
* **Param:**
  name: The resource in the web application that is to be changed.
* **Param:**
  etag: The ETag value of the resource.

#### method *= 'WebApp.SetResourceETag'*

### *class* simatic_s7_webserver_api.WebApp.WebAppSetResourceMediaType(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, app_name: str, name: str, media_type: str)

Constructor used to change the media type of a resoruce from a web application loaded by the user

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  app_name: The name of the web application that contains the resource.
* **Param:**
  name: The resource in the web application that is to be changed.
* **Param:**
  media_type: The media type of the resource.

#### method *= 'WebApp.SetResourceMediaType'*

### *class* simatic_s7_webserver_api.WebApp.WebAppSetResourceModificationTime(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, app_name: str, name: str, last_modified: str)

Constructor to set the modification time of a resource in a web application loaded by the user

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  app_name: The name of the web application that contains the resource.
* **Param:**
  name: The resource in the web application that is to be changed.
* **Param:**
  last_modified: The ISO8601 time stamp as a string, contains the time of the last change.

#### method *= 'WebApp.SetResourceModificationTime'*

### *class* simatic_s7_webserver_api.WebApp.WebAppSetResourceVisibility(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, app_name: str, name: str, visibility: str)

Constructor used to change the visibility of a resource from a web application loaded by the user

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  app_name: The name of the web application that contains the resource.
* **Param:**
  name: The resource in the web application that is to be changed.
* **Param:**
  visibility: The visibility of the resource: public or protected.

#### method *= 'WebApp.SetResourceVisibility'*

### *class* simatic_s7_webserver_api.WebApp.WebAppSetState(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, name: str, state: str)

Constructor that allows you to activate or deactivate a web application that was loaded by the user

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  name: The name of the web application that contains the resource.
* **Param:**
  state: The status of the application, could be enabled (can be reached via HTTP end point) or disabled (cannot be reached via HTTP end point).

#### method *= 'WebApp.SetState'*

## simatic_s7_webserver_api.api module

### *class* simatic_s7_webserver_api.api.ApiBrowse(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### method *= 'Api.Browse'*

#### parse(response: [JsonrpcBaseResponse](#simatic_s7_webserver_api.response.JsonrpcBaseResponse))

Parses the response of a browse request and returns the individual method strings.
If no method is provided or the request failed None is returned.

* **Param:**
  response: The `JsonrpcBaseResponse`
* **Response:**
  A list of all methods that you can call via the Web API with the current firmware.

### *class* simatic_s7_webserver_api.api.ApiBrowseTickets(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, id: str | None = None)

Constructor to know all the tickets of a logged-in user

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  id: the ticket ID that was returned by an API method for use by the ticket system. If no parameter is specified, then the response is componend by all the tickets of the user.

#### method *= 'Api.BrowseTickets'*

#### parse(response: [JsonrpcBaseResponse](#simatic_s7_webserver_api.response.JsonrpcBaseResponse))

Parses the response of a get permissions request and returns a custom object..
If no permission is provided or the request failed None is returned.

* **Param:**
  response: The `JsonrpcBaseResponse`
* **Response:**
  CustomTicket: The [`CustomTicket`](#simatic_s7_webserver_api.api.CustomTicket)

### *class* simatic_s7_webserver_api.api.ApiCloseTicket(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, id: str)

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  id: the ticket ID returned by an API method for use by the ticket system.

#### method *= 'Api.CloseTicket'*

### *class* simatic_s7_webserver_api.api.ApiGetCertificateUrl(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### method *= 'Api.GetCertificateUrl'*

The method outputs a string with a relative URL to the root directory of the CPU Web server ([https://[ip-address](https://[ip-address)]).
If the Web server has not been configured with a CA certificate generated via the global security settings, the method outputs an empty string.

### *class* simatic_s7_webserver_api.api.ApiGetPermissions(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token)

Constructor to know  actions that the user is authorized to do.

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.

#### method *= 'Api.GetPermissions'*

#### parse(response: [JsonrpcBaseResponse](#simatic_s7_webserver_api.response.JsonrpcBaseResponse))

Parses the response of a get permissions request and returns the individual permissions as strings.
If no permission is provided or the request failed None is returned.

* **Param:**
  response: The `JsonrpcBaseResponse`
* **Response:**
  A list of actions for whose execution the user is authorized.

### *class* simatic_s7_webserver_api.api.ApiLogin(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), user: str = 'Anonymous', password: str = '')

Constructor that allows the user to login

* **Param:**
  config: The `RequestConfig`
* **Param:**
  user: the user name.
* **Param:**
  password: the current password.

#### method *= 'Api.Login'*

#### parse(response: [JsonrpcBaseResponse](#simatic_s7_webserver_api.response.JsonrpcBaseResponse))

Parses the response of a login request and returns the user token.
If no user token is found our the request failed None is returned.

* **Param:**
  response: The `JsonrpcBaseResponse` returned by the post
* **Response:**
  The token that indicates that its holder has successfully authenticated themselves at the WebAPI.

### *class* simatic_s7_webserver_api.api.ApiLogout(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token)

Constructor to logout from the Web API session

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.

#### method *= 'Api.Logout'*

### *class* simatic_s7_webserver_api.api.ApiPing(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### method *= 'Api.Ping'*

* **Response:**
  The system outputs a unique ID for the CPU used, teh CPU ID comprises a 28-byte string.

### *class* simatic_s7_webserver_api.api.ApiTicket

Bases: `object`

* **Attribute:**
  id: Ticket ID.
* **Attribute:**
  date_created: ISO8601 time stamp as a string. Time of the ticket creation based on CPU time.
* **Attribute:**
  provider: Name of the method that has created the ticket.
* **Attribute:**
  state: Current ticket status. It could be: ‘created’, ‘active’, ‘completed’ or ‘failed’
* **Attribute:**
  data: additional ticket data. Some methods include additional information to the user.

#### data *= None*

#### date_created *: str*

#### id *: str*

#### provider *: str*

#### state *: [ApiTicketState](#simatic_s7_webserver_api.api.ApiTicketState)*

### *class* simatic_s7_webserver_api.api.ApiTicketState(value, names=<not given>, \*values, module=None, qualname=None, type=None, start=1, boundary=None)

Bases: `Enum`

#### ACTIVE *= 'active'*

#### COMPLETED *= 'completed'*

#### CREATED *= 'created'*

#### FAILED *= 'failed'*

### *class* simatic_s7_webserver_api.api.ApiVersion(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### method *= 'Api.Version'*

Returns the current version number of the Web API

### *class* simatic_s7_webserver_api.api.CustomTicket

Bases: `object`

* **Attribute:**
  max_tickets: maximum number of tickets for one session.
* **Attribute:**
  ticket: The [`ApiTicket`](#simatic_s7_webserver_api.api.ApiTicket)

#### max_tickets *: int*

#### ticket *: [ApiTicket](#simatic_s7_webserver_api.api.ApiTicket)*

## simatic_s7_webserver_api.datalogs module

### *class* simatic_s7_webserver_api.datalogs.DataLogsDownloadAndClear(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, resource: str)

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  resource: The name of the DataLog you want to download. Alternatively, the user can use a path starting with /datalogs/

#### method *= 'DataLogs.DownloadAndClear'*

## simatic_s7_webserver_api.files module

### *class* simatic_s7_webserver_api.files.FilesBaseRequest(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, resource: str)

Constructor used in all these methods related with Files: browse, download, create, delete and create directory

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  resource: Path to the directory or file from the root node. For the root node, the use of a ‘/’ is necessary.

### *class* simatic_s7_webserver_api.files.FilesBrowse(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`FilesBaseRequest`](#simatic_s7_webserver_api.files.FilesBaseRequest)

#### method *= 'Files.Browse'*

#### parse(response: [JsonrpcBaseResponse](#simatic_s7_webserver_api.response.JsonrpcBaseResponse))

Parses the response of a browse files request and returns a list of files with its attributes.

* **Param:**
  response: The `JsonrpcBaseResponse`
* **Response:**
  list compound of files from The [`FilesBrowseEntry`](#simatic_s7_webserver_api.files.FilesBrowseEntry)

### *class* simatic_s7_webserver_api.files.FilesBrowseEntry

Bases: `object`

* **Attribute:**
  name: name of the entry.
* **Attribute:**
  type: type of the entry, either ‘file’ or ‘dir’.
* **Attribute:**
  size: size of the file in bytes (if type is ‘file’).
* **Attribute:**
  last_modified: The ISO8601 time stamp as a string, contains the time of the last change.
* **Attribute:**
  state: reserved for active or inactive DataLogs in the ‘DataLogs’ folder.

#### last_modified *: datetime*

#### name *: str*

#### size *: int | None*

#### state *: str | None*

#### type *: str*

### *class* simatic_s7_webserver_api.files.FilesCreate(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`FilesBaseRequest`](#simatic_s7_webserver_api.files.FilesBaseRequest)

#### method *= 'Files.Create'*

* **Response:**
  This method returns a character string that includes a valid ticket ID.

### *class* simatic_s7_webserver_api.files.FilesCreateDirectory(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`FilesBaseRequest`](#simatic_s7_webserver_api.files.FilesBaseRequest)

#### method *= 'Files.CreateDirectory'*

* **Response:**
  If succesful, the server returns the Boolean value ‘True’

### *class* simatic_s7_webserver_api.files.FilesDelete(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`FilesBaseRequest`](#simatic_s7_webserver_api.files.FilesBaseRequest)

#### method *= 'Files.Delete'*

* **Response:**
  If succesful, the server returns the Boolean value ‘True’

### *class* simatic_s7_webserver_api.files.FilesDeleteDirectory(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`FilesBaseRequest`](#simatic_s7_webserver_api.files.FilesBaseRequest)

#### method *= 'Files.DeleteDirectory'*

* **Response:**
  If succesful, the server returns the Boolean value ‘True’

### *class* simatic_s7_webserver_api.files.FilesDownload(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`FilesBaseRequest`](#simatic_s7_webserver_api.files.FilesBaseRequest)

#### method *= 'Files.Download'*

* **Response:**
  This method returns a character string that includes a valid ticket ID.

### *class* simatic_s7_webserver_api.files.FilesRename(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, resource: str, new_resource: str)

Constructor used to change the name of a file or a directory. It can be used also to move files from one directory to another

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  resource: current  file path or directory path.
* **Param:**
  new_resource: new file path or directory path.

#### method *= 'Files.Rename'*

## simatic_s7_webserver_api.plc module

### *class* simatic_s7_webserver_api.plc.PlcCreateBackup(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str)

Constructor used to request a ticket to create a backup file of the CPU configuration

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.

#### method *= 'Plc.CreateBackup'*

### *class* simatic_s7_webserver_api.plc.PlcOperatingMode(value, names=<not given>, \*values, module=None, qualname=None, type=None, start=1, boundary=None)

Bases: `Enum`

#### HOLD *= 'hold'*

#### RUN *= 'run'*

#### STARTUP *= 'startup'*

#### STOP *= 'stop'*

#### UNKNOWN *= ''*

### *class* simatic_s7_webserver_api.plc.PlcReadOperatingMode(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str)

Constructor used to read the operating mode of the PLC

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.

#### method *= 'Plc.ReadOperatingMode'*

#### parse(response: [JsonrpcBaseResponse](#simatic_s7_webserver_api.response.JsonrpcBaseResponse))

Parses the response of a plc read operating mode request and returns the current status.

* **Param:**
  response: The `JsonrpcBaseResponse`
* **Response:**
  PlcOperatingMode: The class [`PlcOperatingMode`](#simatic_s7_webserver_api.plc.PlcOperatingMode)

### *class* simatic_s7_webserver_api.plc.PlcReadSystemTime(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### method *= 'Plc.ReadSystemTime'*

#### parse(response: [JsonrpcBaseResponse](#simatic_s7_webserver_api.response.JsonrpcBaseResponse))

Parses the response of a plc read system time request and returns the time stamp, if the user synchronized the system time of the CPU,  the time corressponds to the Coordinated Universal Time (UCT).

* **Param:**
  response: The `JsonrpcBaseResponse`
* **Response:**
  datetime: timestamp with USO8601 format as a string.

### *class* simatic_s7_webserver_api.plc.PlcReadTimeSettings(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### method *= 'Plc.ReadTimeSettings'*

* **Response:**
  returns the current active time, the deviation of the time zone from the UCT and any daylight saving time rules.

### *class* simatic_s7_webserver_api.plc.PlcRequestChangeOperatingMode(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, mode: [PlcOperatingMode](#simatic_s7_webserver_api.plc.PlcOperatingMode))

Constructor used to request to change the operating mode of the PLC

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  mode: The [`PlcOperatingMode`](#simatic_s7_webserver_api.plc.PlcOperatingMode)

#### method *= 'Plc.RequestChangeOperatingMode'*

#### parse(response: [JsonrpcBaseResponse](#simatic_s7_webserver_api.response.JsonrpcBaseResponse))

Parses the response of a plc change operating mode request and returns a boolean if the change is satisfied.

* **Param:**
  response: The `JsonrpcBaseResponse`
* **Response:**
  Boolean with ‘True’ value.

### *class* simatic_s7_webserver_api.plc.PlcRestoreBackup(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, password: str)

Constructor used to request a ticket to restore the configuration of a CPU using a backup file.

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  password: the required password for the logged on user, this password must be the same of the user authenticated previously with via the Api.Login method.

#### method *= 'Plc.RestoreBackup'*

## simatic_s7_webserver_api.plcprogram module

### *class* simatic_s7_webserver_api.plcprogram.PlcProgramBrowse(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, mode: str, var: str | None = None)

Constructor used to search for tags and the corresponding metadata according to the individual requirements

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  mode: determines the behavior of this method: ‘var’ information about the specified tag, ‘children’ displays information about the immediate descendants (children) of the specified tags.
* **Param:**
  type: if ‘code_blocks’ reads all code blocks, ‘data_blocks’ reads all the data blocks, ‘tags’ displays all tags.

#### method *= 'PlcProgram.Browse'*

#### parse(response: [JsonrpcBaseResponse](#simatic_s7_webserver_api.response.JsonrpcBaseResponse))

Parses the response of a browse tags request and returns a list of the requested vars.

* **Param:**
  response: The `JsonrpcBaseResponse`
* **Response:**
  PlcProgramBrowseVariable: The [`PlcProgramBrowseVariable`](#simatic_s7_webserver_api.plcprogram.PlcProgramBrowseVariable)

### *class* simatic_s7_webserver_api.plcprogram.PlcProgramBrowseArrayData

Bases: `object`

* **Attribute:**
  start_index: Start index for this array dimension, as specified in the TIA Portal project.
* **Attribute:**
  count: Number of elements in this array dimension.

#### count *: int*

#### start_index *: int*

### *class* simatic_s7_webserver_api.plcprogram.PlcProgramBrowseVariable

Bases: `object`

* **Attribute:**
  name: Start index for this array dimension, as specified in the TIA Portal project.
* **Attribute:**
  address: Address of the tag in STEP 7; only applicable for the tags in the ranges M, I, Q, timer and counter and tags in non-optimized data blocks.
* **Attribute:**
  read_only: Query whether the tag is read-only. The only valid value is ‘True’.
* **Attribute:**
  has_children: Query whether the tag is a structured tag with child tags.
* **Attribute:**
  db_number: Numerical data block identifier. Appears when ‘datatype== datablock’.
* **Attribute:**
  area: Letter which defines the range (M/I/Q/timer/counter) of the tag.
* **Attribute:**
  datatype: data type of the tag
* **Attribute:**
  max_length: If the data type is ‘string’ or ‘wstring’ this value is the maximum number of characters allowed in the tag
* **Attribute:**
  array_dimensions: Object arrays arranged from the most significant to the least significant.

#### address *: str | None*

#### area *: str | None*

#### array_dimensions *: [PlcProgramBrowseArrayData](#simatic_s7_webserver_api.plcprogram.PlcProgramBrowseArrayData) | None*

#### datatype *: str*

#### db_number *: int | None*

#### has_children *: bool | None*

#### max_length *: int | None*

#### name *: str*

#### read_only *: bool | None*

### *class* simatic_s7_webserver_api.plcprogram.PlcProgramRead(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, var: str, mode: str = 'simple')

Constructor used to read a single variable from a CPU

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  var: name of the tag to be read.
* **Param:**
  mode: determines the behavior of this method: ‘simple’ or ‘raw’ and the method will return tag values according to each name representation.

#### method *= 'PlcProgram.Read'*

### *class* simatic_s7_webserver_api.plcprogram.PlcProgramWrite(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), token: str, var: str, value, mode: str = 'simple')

Constructor used to write on a single process tag to a CPU

* **Param:**
  config: The `RequestConfig`
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.
* **Param:**
  var: name of the tag to be written.
* **Param:**
  value: value to be written. It depends on the operating mode.
* **Param:**
  mode: determines the format of value: ‘simple’ or ‘raw’ and the user must specify the values according to each name representation.

#### method *= 'PlcProgram.Write'*

## simatic_s7_webserver_api.request module

### *class* simatic_s7_webserver_api.request.JsonrpcBaseRequest(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: `object`

Represents a base type for all jsonrpc requests against
the SIMATC S7 webserver
Provides all functions to build the request and execute it.

* **Attribute:**
  method: defines the jsonrpc method and functions that are
  defined for the WebAPI
* **Attribute:**
  params: defines additional parameters required by the specific request methods
* **Attribute:**
  address: Address of the PLC webserver, can be either a IPv4/ IPv6 address
  or the DNS name
  Must not contain the protocol definition, this has to be set
  via the protocol attribute
* **Attribute:**
  protocol: defines the protocol (http/https) for connecting to the PLC
* **Attribute:**
  token: Token for authentication and authorization on the PLC
* **Attribute:**
  verifyTls: Switch wether TLS Server Certificate should be verified against
  trusted certificates or trusted by default

#### address *= ''*

#### body()

Creates the body object of the request

#### execute()

#### format_response()

#### headers()

Creates an object for the necessary header fields

#### method *= None*

#### params *= None*

#### parse(response: [JsonrpcBaseResponse](#simatic_s7_webserver_api.response.JsonrpcBaseResponse))

Parses the response of a simple request and returns the
result as a string.
If no result string is provided or the request failed None is returned.
only works for {.. result: “somestring” ..}

* **Param:**
  response: The `JsonrpcBaseResponse`

#### protocol *= ''*

#### request()

Executes the POST request against the webserver

* **Returns:**
  `Response` object
* **Return type:**
  requests.Response

### Raises

requests.RequestException
: There was an ambiguous that occurred while handling your request.

requests.ConnectionError
: A Connection error occurred.

requests.HTTPError
: An HTTP error occurred.

requests.URLRequired
: A valid URL is required to make a request.

requests.TooManyRedirects
: Too many redirects.

requests.ConnectTimeout
: The request timed out while trying to connect to the remote server.
  <br/>
  Requests that produced this error are safe to retry.

requests.ReadTimeout
: The server did not send any data in the allotted amount of time.

requests.Timeout
: The request timed out.
  <br/>
  Catching this error will catch both
  ConnectTimeout and ReadTimeout errors.

requests.JSONDecodeError
: Couldn’t decode the text into json

#### response *: Response | None* *= None*

#### token *= None*

#### url()

Creates the url based on the information address and protocol

#### verifyTls *= True*

### *class* simatic_s7_webserver_api.request.RequestConfig

Bases: `object`

Base configuration for all requests

* **Attribute:**
  address: Address of the PLC webserver, can be either a IPv4/ IPv6 address
  or the DNS name
  Must not contain the protocol definition, this has to be set
  via the protocol attribute
* **Attribute:**
  protocol: defines the protocol (http/https) for connecting to the PLC
* **Attribute:**
  verifyTls: Switch wether TLS Server Certificate should be verified against
  trusted certificates or trusted by default

#### address *= ''*

#### protocol *= ''*

#### verifyTls *= True*

## simatic_s7_webserver_api.response module

### *class* simatic_s7_webserver_api.response.JsonrpcBaseResponse

Bases: `object`

Base type for all responsed returned by the SIMATIC S7 Webserver

* **Attribute:**
  error: Generic type for error if there is one, else None
* **Attribute:**
  result: Object that provides result data
* **Attribute:**
  raw: Generic HTTP response

#### \_\_init_\_()

#### error *: [JsonrpcError](#simatic_s7_webserver_api.response.JsonrpcError) | None*

#### is_error()

#### *static* parse(response: Response)

Tries to parse a generic HTTP response into the specific jsonrpc
response format. Returns None if parsing is not successfull

* **Param:**
  response: Generic HTTP response

#### raw *: Response*

#### result *: None*

### *class* simatic_s7_webserver_api.response.JsonrpcError(http_code: int, code: int = -1, message: str | None = None)

Bases: `object`

Base type for all errors returned by the SIMATIC S7 Webserver

* **Attribute:**
  code: Code of the error, defined in webserver documentation
* **Attribute:**
  message: Optional additional information provided by the Webserver
* **Attribute:**
  http_code: HTTP Response code provided by the server response

#### \_\_init_\_(http_code: int, code: int = -1, message: str | None = None)

Constructor for the error type

* **Param:**
  http_code: HTTP Response code provided by the server response
* **Param:**
  code: Optional code of the error, defined in webserver documentation
* **Param:**
  message: Optional additional information provided by the Webserver

#### code *: int*

#### http_code *: int*

#### message *: str | None*

## simatic_s7_webserver_api.ticket module

### *class* simatic_s7_webserver_api.ticket.TicketDownloadData(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`JsonrpcBaseRequest`](#simatic_s7_webserver_api.request.JsonrpcBaseRequest)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), ticket_id: str, token: str | None = None)

Constructor used to download data from the CPU

* **Param:**
  config: The `RequestConfig`
* **Param:**
  ticket_id: ticket ID generated in a method that needs to work with the ticket management system.
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.

#### body()

Overwrites the body method of base request.
No body is needed for ticket requests

#### execute()

#### method *= 'NotUsed'*

#### request()

Executes the POST request against the webserver

* **Returns:**
  `Response` object
* **Return type:**
  requests.Response

### Raises

requests.RequestException
: There was an ambiguous that occurred while handling your request.

requests.ConnectionError
: A Connection error occurred.

requests.HTTPError
: An HTTP error occurred.

requests.URLRequired
: A valid URL is required to make a request.

requests.TooManyRedirects
: Too many redirects.

requests.ConnectTimeout
: The request timed out while trying to connect to the remote server.
  <br/>
  Requests that produced this error are safe to retry.

requests.ReadTimeout
: The server did not send any data in the allotted amount of time.

requests.Timeout
: The request timed out.
  <br/>
  Catching this error will catch both
  ConnectTimeout and ReadTimeout errors.

requests.JSONDecodeError
: Couldn’t decode the text into json

#### url()

Creates the url based on the information address and protocol
Differs from base JSONRPC request in the route params

### *class* simatic_s7_webserver_api.ticket.TicketUploadData(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), \*args, \*\*kwargs)

Bases: [`TicketDownloadData`](#simatic_s7_webserver_api.ticket.TicketDownloadData)

#### \_\_init_\_(config: [RequestConfig](#simatic_s7_webserver_api.request.RequestConfig), ticket_id: str, data: bytes, token: str | None = None)

Constructor used to upload data to the CPU

* **Param:**
  config: The `RequestConfig`
* **Param:**
  ticket_id: ticket ID generated in a method that needs to work with the ticket management system.
* **Param:**
  data: data that is going to be uploaded. It must be in bytes format.
* **Param:**
  token: The user token that identifies the user as successfully authenticated with its permissions.

#### data *= b''*

#### execute()

#### headers()

Creates an object for the necessary header fields

#### method *= 'NotUsed'*

#### request()

Executes the POST request against the webserver

* **Returns:**
  `Response` object
* **Return type:**
  requests.Response

### Raises

requests.RequestException
: There was an ambiguous that occurred while handling your request.

requests.ConnectionError
: A Connection error occurred.

requests.HTTPError
: An HTTP error occurred.

requests.URLRequired
: A valid URL is required to make a request.

requests.TooManyRedirects
: Too many redirects.

requests.ConnectTimeout
: The request timed out while trying to connect to the remote server.
  <br/>
  Requests that produced this error are safe to retry.

requests.ReadTimeout
: The server did not send any data in the allotted amount of time.

requests.Timeout
: The request timed out.
  <br/>
  Catching this error will catch both
  ConnectTimeout and ReadTimeout errors.

requests.JSONDecodeError
: Couldn’t decode the text into json

## simatic_s7_webserver_api.util module

### simatic_s7_webserver_api.util.get_array_named_values(response: [JsonrpcBaseResponse](#simatic_s7_webserver_api.response.JsonrpcBaseResponse))

Function used to manage a response and extract what is inside of each “name” index.

* **Param:**
  response: The `JsonrpcBaseResponse`

## Module contents
