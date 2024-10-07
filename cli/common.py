from simatic_s7_webserver_api.request import JsonrpcBaseRequest, RequestConfig
from simatic_s7_webserver_api.api import ApiLogin, ApiLogout
import logging

def post_or_panic(req: JsonrpcBaseRequest, logger: logging.Logger, message: str = ""):
    logger.debug(req)
    try:
        res = req.execute()
        logger.debug(req.format_response())
        return req.parse(res)
    except Exception as e:
        logger.error(message)
        logger.error(str(e))
        return

def login(config: RequestConfig, logger:logging.Logger, username: str, password: str) -> str|None:
    req = ApiLogin(config, username, password)
    return req.execute()

def logout(config: RequestConfig, logger: logging.Logger,token) -> bool:
    res = ApiLogout(config, token).execute()
    if res is None:
        return False

    return bool(res)
