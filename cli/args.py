from enum import Enum


class CliAction(Enum):
    UNKNOWN = 0
    BACKUP = 1
    RESTORE = 2
    PING = 3
    PERMISSIONS = 4
    OPMODE = 7
    INFO = 8
    FILES = 9
class CliArguments:
    Action = CliAction.UNKNOWN
    Args = object
    Address = ""
    Username = ""
    Password = ""
    Filename = ""
    RemotePath = ""
    Verbose = False
    Debug = False
    Silent = False
    PrintHelp = False
    ForceAction = False

def printUsage():
    print("Usage backup.py <ACTION> [OPTIONS]")
    
    print("\n━━ Actions ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ \n")
    print("backup       Retrieves a binary backup file of the current PLC image for later restore; requires a PLC Stop during the backup phase\n")
    print("restore      Restores a previous PLC state from a binary backup file of the PLC, requires a restart of the PLC and reinitializes all variables\n")
    print("ping         Tries to reach the PLC WebApi to check if it is accessible and active for further action\n")
    print("permissions  Retrieves all the API permission the provided user has available\n")
    print("opmode       Changes the operating mode to either start|stop. Stops/ Starts the PLC Program execution and may lead to dangerous situations.\n")
    print("info         Prints information about the WebApi Version, local system time as well as available methods\n")
    print("files        Utility to interact (browse|upload|download|delete) files on the S7 1500 memory card \n")
    print(
        "\nCommand line tool for automation of common maintenance tasks for the S7 1500 PLC using the WebAPI\n"
    )
    print("\n━━ Options ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ \n")
    print("  --debug\tEnable debug logging level for developer information")
    print("  --verbose\tEnable verbose logging for further information")
    print("  --silent\tDisable all logging for non-error messages")

def parse(args):

    if args is None or len(args) <= 1:
        printUsage()
        exit(1)

    action = CliAction.UNKNOWN

    match args[1]:
        case "--help":
            printUsage()
            exit(1) 
        case "backup":
            action =  CliAction.BACKUP
        case "restore":
            action = CliAction.RESTORE
        case "ping":
            action = CliAction.PING
        case "permissions":
            action = CliAction.PERMISSIONS
        case "opmode":
            action = CliAction.OPMODE
        case "info":
            action = CliAction.INFO
        case "files":
            action = CliAction.FILES
        case _:
            printUsage()
            exit(1)

    infos = CliArguments()
    infos.Action = action
    printHelp = False

    infos.Args = [args[i] for i in range(2,len(args))]

    for i in range(1, len(args)):
        match args[i]:
            case "--password":
                infos.Password = args[i + 1]
            case "--user":
                infos.Username = args[i + 1]
            case "--address":
                infos.Address = args[i + 1]
            case "--file":
                infos.Filename = args[i + 1]
            case "--verbose":
                infos.Verbose = True
            case "--debug":
                infos.Debug = True
            case "--silent":
                infos.Silent = True
            case "--remote-path":
                infos.RemotePath = args[i + 1]
            case "--help":
                infos.PrintHelp = True
            case "--force":
                infos.ForceAction = True

    return infos


