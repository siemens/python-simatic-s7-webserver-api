from simatic_s7_webserver_api.request import RequestConfig
from cli.clicommand import CliCommandAuthenticated
from cli.args import CliArguments
from cli.common import login
from simatic_s7_webserver_api.plc import PlcRequestChangeOperatingMode, PlcReadOperatingMode
from cli.vars import LOGGING_SUCCESS
from logging import Logger
from simatic_s7_webserver_api.api import ApiBrowseTickets
from simatic_s7_webserver_api.ticket import TicketDownloadData, TicketUploadData
from simatic_s7_webserver_api.files import FilesBrowse, FilesCreate, FilesDelete, FilesDownload
import time

class CliCommandFiles(CliCommandAuthenticated):

    def __init__(self, args: CliArguments, logger: Logger, config: RequestConfig) -> None:
        super().__init__(args, logger, config)

    def validate_args(self):
        if not super.validate_args(self.args):
            self.logger.error("Missing IP Address or DNS name of webserver, required for requests")
            return False
        if self.args.Args is None or len(self.args.Args) == 0 or self.args.Args[0] != "upload" and self.args.Args[0] != "download" and args.Args[0] != "browse" and args.Args[0] != "delete":
            logger.error("Not enough positional arguments, requires one positional argument [upload | download | browse | delete]")
            return False
        if args.Filename is None and (args.Args[0] == "upload" or args.Args[0] == "download"):
            logger.error("No filename for local target file is given")
            return False
        if args.RemotePath is None:
            logger.error("No  for local target file is given")
            return False
        if args.Address is None or args.Username is None or args.Password is None:
            logger.error("General endpoint information missing")
            return False
        
        return True

    def execute(self):
        
        token = login(self.config, self.logger, self.args.Username, self.args.Password)

        if token is None:
            self.logger.error("Logging in failed, check debug logs for further info")
            return

        match self.args.Args[0]:
            case "browse":
                self.logger.info("Selected browse, will browse for files")

                result = FilesBrowse(self.config, token, self.args.RemotePath)
                self.logger.log(LOGGING_SUCCESS, result)
            case "upload":
                self.logger.info("Selected file upload")

                upload_file_ticket = FilesCreate(self.config, token, resource=self.args.RemotePath).execute()
                
                if upload_file_ticket is None:
                    self.logger.error("Unable to retrieve ticket for upload, make sure that the user has the correct credentials, the directory exists and the file is not present")
                    return

                tickets = ApiBrowseTickets(self.config, token, id=upload_file_ticket).execute()
                if tickets is None or len(tickets) <=0:
                    self.logger.error("Unable to retrieve ticket for upload")
                    return
                time.sleep(1)
                with open(self.args.Filename, "rb") as file:
                    response = TicketUploadData(self.config,  tickets[0].id, file.read(), token=token).execute()
                
                if response is None:
                    self.logger.error("Returned content for upload is null, check response error")
                    return

                self.logger.log(LOGGING_SUCCESS, f"Successfully uploaded the file {self.args.Filename} to the PLC")

            case "download":
                self.logger.info("Selected file download")

                download_file_ticket = FilesCreate(self.config, token, resource=self.args.RemotePath).execute()
                
                if download_file_ticket is None:
                    self.logger.error("Unable to retrieve ticket for downloading a file, make sure that the user has the correct credentials and the directory and file exists")
                    return

                tickets = ApiBrowseTickets(self.config, token, id=download_file_ticket).execute()
                if tickets is None or len(tickets) <=0:
                    self.logger.error("Unable to retrieve ticket for downloading")
                    return
                time.sleep(1)

                response = TicketDownloadData(self.config, ticket_id=tickets[0].id).execute()

                with open(self.args.Filename, "wb") as file:
                    file.write(response)

                if response is None:
                    self.logger.error("Returned content for download is null, check response error")
                    return

                self.logger.log(LOGGING_SUCCESS, f"Successfully downloaded the file {self.args.Filename} from the PLC")
            
            case "delete":
                self.logger.info("Selected to delet file {self.args.RemotePath}")

                delete_file_ticket = FilesDelete(self.config, token, resource= self.args.RemotePath)

                
    def help():
        print("\n━━ Usage ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ \n")
        print("main.py opmode [upload | download | browse | delete] --address <S7 1500 Address> --user <Username> --password <Password> --file <local file> --remote-path <file on plc>")
        print("\n━━ Actions ━━━━━━━━━━━━━━━━━━━━━━━━━━ \n")
        print("upload      Uploads a local file to a location on the PLCs memory card, directories in the path on the memory card must exist")
        print("download    Downloads a remote file from the memory card of the PLC to the PC, file must exist on the memory card")
        print("browse      Browses a directory on the PLC memory card and displays available files")
        print("delete      Deletes a file on the memory card")
        print("\n━━ Options ━━━━━━━━━━━━━━━━━━━━━━━━━━ \n")
        print("--force    Forces the PLC to Operating Mode Stop if required, may lead to dangerous machine state!")
        print("--verbose  Showing additional information on the console output")
        print("--debug    Showing debug information on the console output")
        print("--silent   Showing no output on the commandline, overwritten by verbose or debug")
        print("━━ Examples ━━━━━━━━━━━━━━━━━━━━━━━━━ \n")
        print("Upload a file to the PLC")
        print(" $ main.py files upload --address \"192.168.0.1\" --user \"siemens\" --password \"securepassword\" --file \"./local.txt\" --remote-path \"/local.txt\"\n")
        print("download")
        print(" $ main.py opmode run --address \"192.168.0.1\" --user \"siemens\" --password \"securepassword\"")
