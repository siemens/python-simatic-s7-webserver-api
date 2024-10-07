# S7 1500 WebApi Pylib

This application example provides a convenience wrapper library for interacting with the S7 1500 Webserver REST API in a custom Python script.

The library includes all methods supported in S7 1500 with Firmware V3.0. Further methods will be added as newer firmware versions are released. The library itself does not contain any internal logic and only provides types and classes to simplify interaction with the webserver in a custom script.

While the library facilitates interaction with the S7 1500 Webserver API, we also provide a Command Line Interface (CLI) for various predefined functions to interact with the API. The CLI script is located in the cli/ folder and offers several functionalities for managing the PLC.

## CLI Functionalities

The CLI provides the following actions:

- **backup**: Retrieves a binary backup file of the current PLC image for later restore; requires a PLC stop during the backup phase.
- **restore**: Restores a previous PLC state from a binary backup file; requires a restart of the PLC and reinitializes all variables.
- **ping**: Checks the accessibility and activity of the PLC WebAPI.
- **permissions**: Retrieves all API permissions available to the provided user.
- **opmode**: Changes the operating mode to either start or stop; stops/starts PLC program execution, which may lead to dangerous situations.
- **info**: Prints information about the WebAPI version, local system time, and available methods.
- **files**: Interacts with files on the S7 1500 memory card (browse, upload, download, delete).

## Prerequisites

The Python script can run on any system with **Python 3** installed. The library has a dependency on `urllib3`, which is automatically installed as a dependency of the `requests` library. 

To install the library and its dependencies, use:

```bash
pip install python-simatic-step7-webserver-api
```

With this setup, you can start using the library by following the Example of usage section.

If you want to use the cli functionality, in this current version there are no entrypoints defined so yo need to  work using the main script. In the next section, some examples are provided.


Another option available is getting the code, you can also clone or download the repository. This can be done by clicking on the button <> Code and either selecting Download ZIP or executing the following command in your command line:

```bash
git clone https://github.com/siemens/python-simatic-step7-webserver-api

```
This command will create a new folder that you can enter with:

```bash
cd python-simatic-step7-webserver-api
```
From here, you are ready to get started with the next steps.

## Getting Started with CLI

The CLI python script logic is located in the folder `cli/` and can be started with the command

```bash
python main.py --help
```
This will print the usage help for the cli tool that contains some functionality that interacts with the web API using this api library.

Here there are some examples using this tool:

```bash
python main.py "stop" --user "Admin" --password "12345678Aa" --ip "192.168.0.1"

python main.py "start" --user "Admin" --password "12345678Aa" --ip "192.168.0.1"

python main.py "info" --user "Admin" --password "12345678Aa" --ip "192.168.0.1"

python main.py "browse" --user "Admin" --password "12345678Aa" --ip "192.168.0.1"
```

## Example of usage with API

```bash
config = api.request.RequestConfig()
config.address = "192.168.0.1"
config.protocol = "https"
config.verifyTls = False

name_app = "app1"
name_resource = "Logo"
token = api.ApiLogin(config, "General", "12345678Aa").execute()
new_app = api.WebApp.WebAppCreate(config, token, "app1","enabled")
create_resource = api.WebApp.WebAppCreateResource(config, token, "app1","Logo","image/jpeg", "2024-10-09T13:12:06Z")  

ticket_resource = create_resource.execute()


with open("C:/Users/User1/Desktop/Logo.jpeg",'rb') as file:
  data = file.read()   
  upload_archive = api.ticket.TicketUploadData(config,ticket_resource, data, token)
  print(subir_archivo.execute())

```

This is an example to upload a file called `Logo.jpeg` from a local machine to the webserver using the ticketing system after doing a login, creating the app, the resource and uploading it.



## License
The S7 1500 WebApi Pylib is licensed under the MIT License , which means that you are free to get and use it for commercial and non-commercial purposes as long as you fulfill its conditions.

See the [LICENSE.md](LICENSE.md) file for more details.


