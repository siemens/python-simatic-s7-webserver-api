from simatic_s7_webserver_api.request import RequestConfig
from cli.clicommand import CliCommand
from cli.args import CliArguments
from cli.common import login
from simatic_s7_webserver_api.plc import PlcRequestChangeOperatingMode, PlcReadOperatingMode
from cli.vars import LOGGING_SUCCESS
from logging import Logger

class CliCommandOpmode(CliCommand):

    def __init__(self, args: CliArguments, logger: Logger, config: RequestConfig) -> None:
        super().__init__(args, logger, config)

    def validate_args(self):
        if self.args.Filename is None:
            self.logger.error("No filename for target file to restore is given")
            return False
        if self.args.Address is None or self.args.Username is None or self.args.Password is None:
            self.logger.error("General endpoint information missing")
            return False
        if self.args.Args is None or len(self.args.Args) == 0 or self.args.Args[0] != "start" and self.args.Args[0] != "stop" and self.args.Args[0] != "read":
            self.logger.error("Not enough positional arguments, requires one positional argument [read | stop | run]")
            return False
        return True

    def execute(self):

        self.logger.info("Selected to {0} operating mode".format(self.args.Args[0]))

        token = login(self.config, self.logger, self.args.Username, self.args.Password)
        if token is None:
            self.logger.error("Unable to log in to the PLC")
            return
        opmode = ""
        match self.args.Args[0]:
            case "read":
                opmode = PlcReadOperatingMode(self.config, token).execute()
                assert opmode is not None
                self.logger.log(LOGGING_SUCCESS, f"PLC is in {opmode.value}")
                return
            case "run":
                opmode = PlcRequestChangeOperatingMode(self.config, token, self.args.Args[0]).execute()
            case "stop":
                opmode = PlcRequestChangeOperatingMode(self.config, token, self.args.Args[0]).execute()

        assert opmode is not None

        if opmode:
            self.logger.log(LOGGING_SUCCESS, f"Successfully changed operating mode to {self.args.Args[0]}")
        else:
            self.logger.error("Unable to change operating mode")

                
    def help():
        print("\n━━ Usage ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ \n")
        print("main.py opmode [read | stop | run] --address <S7 1500 Address> --user <Username> --password <Password> --file <Restorefile>")
        print("\n━━ Actions ━━━━━━━━━━━━━━━━━━━━━━━━━━ \n")
        print("read       Reads the current operating mode of the PLC, does not change the operating mode")
        print("stop       Sets the PLC Operating Mode to stop, may lead to dangerous machine state!")
        print("start      Sets the PLC Operating Mode to start, may lead to dangerous machine state!")
        print("\n━━ Options ━━━━━━━━━━━━━━━━━━━━━━━━━━ \n")
        print("--force    Forces the PLC to Operating Mode Stop if required, may lead to dangerous machine state!")
        print("--verbose  Showing additional information on the console output")
        print("--debug    Showing debug information on the console output")
        print("--silent   Showing no output on the commandline, overwritten by verbose or debug")
        print("━━ Examples ━━━━━━━━━━━━━━━━━━━━━━━━━ \n")
        print("Setting the PLC Operating Mode to STOP")
        print(" $ main.py opmode stop --address \"192.168.0.1\" --user \"siemens\" --password \"securepassword\"\n")
        print("Setting the PLC Operating Mode to RUN")
        print(" $ main.py opmode run --address \"192.168.0.1\" --user \"siemens\" --password \"securepassword\"")
