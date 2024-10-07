from cli.clicommand import CliCommand
from simatic_s7_webserver_api.plc import PlcReadOperatingMode, PlcOperatingMode, PlcRequestChangeOperatingMode, PlcCreateBackup, PlcRestoreBackup
from simatic_s7_webserver_api.api import ApiBrowseTickets
from simatic_s7_webserver_api.ticket import TicketDownloadData, TicketUploadData
from cli.common import login
from cli.vars import LOGGING_SUCCESS
from cli.args import CliArguments 
import time
import sys
import logging

class CliCommandBackup(CliCommand):
    def validate_args(self, logger: logging.Logger, args: CliArguments):
        if args.Filename is None:
            logger.error("No filename for target backup file given")
            return False
        if args.Address is None or args.Username is None or args.Password is None:
            logger.error("General endpoint information missing")
            return False
        return True

    def execute(self):
        
        if self.args.PrintHelp:
            CliCommandBackup.help()
            sys.exit(0)
        
        self.logger.info("Selected create backup")
        token = login(self.config, self.logger, self.args.Username, self.args.Password)
        if token is None:
            self.logger.error("Unable to log in to the PLC")
            return

        if not self.args.ForceAction:
            opmode = None
            try:
                opmode = PlcReadOperatingMode(self.config, token).execute()
            except:
                self.logger.error("Unable to get operating mode of PLC, make sure PLC is in stop or force update")
                return

            if opmode != PlcOperatingMode.STOP and not self.args.ForceAction: 
                self.logger.error("PLC is not stopped and force flag is not set, make sure PLC is in stop")
                return
        else:
            opmode = PlcRequestChangeOperatingMode(self.config, token, PlcOperatingMode.STOP).execute()

        create_backup = PlcCreateBackup(self.config, token).execute()
        
        if create_backup is None:
            self.logger.error("Unable to retrieve ticket for backup, make sure PLC is in stop")
            return

        tickets = ApiBrowseTickets(self.config, token).execute()
        if tickets is None or len(tickets) <=0:
            self.logger.error("Unable to retrieve ticket for backup, make sure PLC is in stop")
            return
        time.sleep(1)

        response = TicketDownloadData(self.config, ticket_id=tickets[0].id).execute()

        if response is None:
            self.logger.error("Returned content for backup is null, check response error")
            return

        with open(self.args.Filename, "wb") as file:
            file.write(response)

        self.logger.log(LOGGING_SUCCESS, f"Successfully downloaded the backup file {self.args.Filename}")

    def help():
        print("\n━━ Usage ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ \n")
        print("main.py backup --address <S7 1500 Address> --user <Username> --password <Password> --file <Outputfile>")
        print("\n━━ Options ━━━━━━━━━━━━━━━━━━━━━━━━━━ \n")
        print("--force    Forces the PLC to Operating Mode Stop if required, may lead to dangerous machine state!\n")
        print("--verbose  Showing additional information on the console output\n")
        print("--debug    Showing debug information on the console output\n")
        print("--silent   Showing no output on the commandline, overwritten by verbose or debug\n")
        print("━━ Examples ━━━━━━━━━━━━━━━━━━━━━━━━━ \n")
        print(" $ main.py backup --address \"192.168.0.1\" --user \"siemens\" --password \"securepassword\" --file \"./directory/file\" --force")

class CliCommandRestore(CliCommand):
    def validate_args(self,logger: logging.Logger, args: CliArguments):
        if args.Filename is None:
            logger.error("No filename for target file to restore is given")
            return False
        if args.Address is None or args.Username is None or args.Password is None:
            logger.error("General endpoint information missing")
            return False
        return True

    def execute(self):
        
        if self.args.PrintHelp:
            CliCommandRestore.help()
            sys.exit(0)
        self.logger.info("Selected create restore")
        token = login(self.config, self.logger, self.args.Username, self.args.Password)
        if token is None:
            self.logger.error("Unable to log in to the PLC")
            return

        if not self.args.ForceAction:
            opmode = None
            try:
                opmode = PlcReadOperatingMode(self.config, token).execute()
            except:
                self.logger.error("Unable to get operating mode of PLC, make sure PLC is in stop or force update")
                return

            if opmode != PlcOperatingMode.STOP and not self.args.ForceAction: 
                self.logger.error("PLC is not stopped and force flag is not set, make sure PLC is in stop")
                return
        else:
            opmode = PlcRequestChangeOperatingMode(self.config, token, PlcOperatingMode.STOP).execute()

        restore_backup = PlcRestoreBackup(self.config, token, self.args.Password).execute()
        
        if restore_backup is None:
            self.logger.error("Unable to retrieve ticket for restore, make sure PLC is in stop")
            return

        tickets = ApiBrowseTickets(self.config, token).execute()
        if tickets is None or len(tickets) <=0:
            self.logger.error("Unable to retrieve ticket for restore, make sure PLC is in stop")
            return
        time.sleep(1)
        with open(self.args.Filename, "wb") as file:
            response = TicketUploadData(self.config,  tickets[0].id, file.read(), token=token).execute()
        
        if response is None:
            self.logger.error("Returned content for restore is null, check response error")
            return

        self.logger.log(LOGGING_SUCCESS, f"Successfully uploaded the backup file {self.args.Filename} to the PLC")

        
    def help():
        print("\n━━ Usage ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ \n")
        print("main.py restore --address <S7 1500 Address> --user <Username> --password <Password> --file <Restorefile>")
        print("\n━━ Options ━━━━━━━━━━━━━━━━━━━━━━━━━━ \n")
        print("--force    Forces the PLC to Operating Mode Stop if required, may lead to dangerous machine state!\n")
        print("--verbose  Showing additional information on the console output\n")
        print("--debug    Showing debug information on the console output\n")
        print("--silent   Showing no output on the commandline, overwritten by verbose or debug\n")
        print("━━ Examples ━━━━━━━━━━━━━━━━━━━━━━━━━ \n")
        print(" $ main.py restore --address \"192.168.0.1\" --user \"siemens\" --password \"securepassword\" --file \"./directory/file\"")
