import logging
import sys

from common.constants import *

def get_logger(name, level=logging.INFO, stream_handler=sys.stdout, log_name="log.log",
               formatter='%(asctime)s [%(levelname)s] %(name)s: %(message)s'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(formatter)
    stream_handler = logging.StreamHandler(stream_handler)
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    log_path = Constants.Logs_Folder
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    
    file_handler = logging.FileHandler(Constants.Logs_Folder+log_name)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger