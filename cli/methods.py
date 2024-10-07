import datetime
import time
import logging

from simatic_s7_webserver_api.api import ApiBrowse, ApiBrowseTickets, ApiGetPermissions, ApiLogout, ApiPing, ApiLogin, ApiTicket, ApiTicketState, ApiVersion
from simatic_s7_webserver_api.files import FilesBrowse, FilesCreate
from simatic_s7_webserver_api.plc import PlcCreateBackup, PlcOperatingMode, PlcReadOperatingMode, PlcReadSystemTime, PlcRequestChangeOperatingMode, PlcRestoreBackup
from simatic_s7_webserver_api.plcprogram import PlcProgramBrowse, PlcProgramBrowseVariable 
from simatic_s7_webserver_api.request import RequestConfig, JsonrpcBaseRequest
from simatic_s7_webserver_api.response import JsonrpcBaseResponse
from simatic_s7_webserver_api.ticket import  TicketDownloadData, TicketUploadData
from cli.args import CliArguments
from cli.vars import LOGGING_SUCCESS
from cli.common import login, logout

def ping(config: RequestConfig, logger: logging.Logger):

    logger.info("Selected ping, will try to reach the PLC Webserver")

    while(1):

        start = time.time_ns()
        
        res = ApiPing(config).execute()      
        
        duration = (time.time_ns() - start) //1000000 
        logger.log(LOGGING_SUCCESS, f'PLC available and responded within {duration:3d}ms')
        time.sleep(1)

def permissions(config: RequestConfig, args: CliArguments, logger: logging.Logger):
    logger.info("Selected permissions, will query available user permissions")
    
    token = login(config, logger, args.Username, args.Password)

    permissions = ApiGetPermissions(config, token).execute()

    if permissions is None:
        logger.error("Permissions could not be received, check credentials")
        return

    print(f"Permission for user {args.Username}")
    print(f"-----------------------------------")
    for permission in permissions:
       print("\t",permission) 

def info(config: RequestConfig, logger: logging.Logger):
    logger.info("Selected info, will query for API information")

    methods = ApiBrowse(config).execute()

    if methods is None:
        logger.error("Methods could not be received")
        return

    version = ApiVersion(config).execute()
    timestamp = PlcReadSystemTime(config).execute()

    assert timestamp is not None
    
    deviation = datetime.datetime.now() - timestamp
    print(f"Endpoint {config.address} is available with the API version {version}")
    print(f"PLC has local system time {timestamp} with deviation of local system of {deviation}")
    print(f"Available methods on endpoint {config.address}")
    print(f"-----------------------------------")
    for method in methods:
       print("\t",method) 

    
def browse_tickets(config: RequestConfig, args: CliArguments, logger: logging.Logger):
    logger.info("Selected browse tickets, will browse for currently open tickets")
    token = login(config, logger, args.Username, args.Password)

    if token is None:
        logger.error("Unable to log in to the PLC")
        return
    
    tickets = ApiBrowseTickets(config, token).execute() 

    assert tickets is not None

    if len(tickets) <= 0:
        logger.warning("No tickets currently active in the webserver")
        exit(0)
    print(f"\tName\t|\tType\t|\tAddress\t|")
    for var in tickets:
        print(f"\t{var.id}\t|\t{var.provider}\t|\t{var.date_created}\t|\t{var.state}\t|")

    

