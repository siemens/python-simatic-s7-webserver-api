import sys
import logging
from cli.args import CliArguments
from cli.vars import LOGGING_SUCCESS
from simatic_s7_webserver_api.request import RequestConfig

class CliCommand():

    logger: logging.Logger
    args: CliArguments
    config: RequestConfig

    def __init__(self, args: CliArguments, logger: logging.Logger, config: RequestConfig) -> None:
        self.logger = logger
        if logger is None:
            print("Logger is not set, creating default logger")
            formatter = logging.Formatter('%(levelname)s - %(message)s')
            logging.addLevelName(LOGGING_SUCCESS, "SUCCESS")
            logger = logging.getLogger("stdout")
            logger.setLevel(logging.INFO)
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)
            self.logger = logger
        
        if args is None:
            self.logger.fatal("CLI Arguments not present, exiting now...")
            sys.exit(1)
        
        if config is None:
            self.logger.fatal("Request configuration is empty, exiting now...")
            sys.exit(1)

        if not type(self).validate_args(logger, args) or args.PrintHelp:
            type(self).help()
            sys.exit(1)

        self.args = args
        self.config = config

    def validate_args(self) -> bool:
        if self.args.Address is None or self.args.Address == "":
            self.logger.error("Missing mandatory argument Address containing")
            return False
        return True

    def execute(self):
        self.logger.fatal("Method not implemented yet, exiting now...")
        sys.exit(1)

    def help(self):
        self.logger.fatal("Help is not implemented for this method, exiting now...")
        sys.exit(1)

class CliCommandAuthenticated(CliCommand):
    def __init__(self, args: CliArguments, logger: logging.Logger, config: RequestConfig) -> None:
        super().__init__(args, logger, config)
    
    def validate_args(self) -> bool:
        if not CliCommand.validate_args():
            return False
        
        if self.args.Password is None or self.args.Password == "" or self.args.Username is None or self.args.Username == "":
            return False

        return True