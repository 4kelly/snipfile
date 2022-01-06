import logging

logger = logging.getLogger("snippet")
handler = logging.StreamHandler()
logger.level = logging.DEBUG

logger.addHandler(handler)
