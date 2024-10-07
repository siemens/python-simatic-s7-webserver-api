from typing import List
import requests
import random
import re
from datetime import datetime, time
import urllib3
import sys
import signal
import time
import logging
from simatic_s7_webserver_api.api import ApiBrowseTickets, ApiCloseTicket, ApiLogin
from simatic_s7_webserver_api.plc import PlcOperatingMode 
from simatic_s7_webserver_api.request import RequestConfig
import simatic_s7_webserver_api.WebApp
from cli.args import CliAction
import cli.methods
import cli.args
import cli.vars
import cli.backuprestore
import cli.opmode
import cli.files

def signal_handler(sig, frame):
    print("User cancelled execution")
    sys.exit(0)

# ------------------------------------------
if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    signal.signal(signal.SIGINT, signal_handler)

    args = cli.args.parse(sys.argv)

    level = logging.ERROR

    if not args.Silent:
        level = cli.vars.LOGGING_SUCCESS
        if args.Verbose: 
            level = logging.INFO
        if args.Debug:
            level = logging.DEBUG   

    formatter = logging.Formatter('%(levelname)s - %(message)s')
    logging.addLevelName(cli.vars.LOGGING_SUCCESS, "SUCCESS")
    logger = logging.getLogger("stdout")
    logger.setLevel(level)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # logger.add(sys.stdout, format="{level}: {message}", level=level, colorize=True)
    logger.debug(f"Selected action {args.Action} for user {args.Username} on address {args.Address}")
        
    config = RequestConfig()
    config.verifyTls = False
    config.protocol = "https"
    config.address = args.Address

    token = None

    match args.Action:
        case CliAction.BACKUP:
            """ cli.methods.plc_create_backup(config, args, logger, force=True) """
            cli.backuprestore.CliCommandBackup(args, logger, config).execute()
        case CliAction.RESTORE:
            cli.backuprestore.CliCommandRestore(args, logger, config).execute()
        case CliAction.PING:
            cli.methods.ping(config, logger)
        case CliAction.PERMISSIONS:
            cli.methods.permissions(config, args, logger)
        case CliAction.INFO:
            cli.methods.info(config, logger)
        case CliAction.OPMODE:
            cli.opmode.CliCommandOpmode(args, logger, config).execute()
        case CliAction.FILES:
            cli.files.CliCommandFiles(args, logger, config).execute()

    token = ApiLogin(config, args.Username, args.Password).execute()
    assert token is not None
    logger.info(f"Cleaning up and closing open tickets")
    tickets = ApiBrowseTickets(config, token).execute()
    
    if tickets is not None:
        for ticket in tickets:
            if "id" in ticket:
                logger.info(f"Closing ticket {ticket.id}")
                ApiCloseTicket(config, token, ticket.id).execute()

    cli.methods.logout(config, logger, token)

