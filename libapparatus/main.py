"""libapparatus/helper.py"""
import json
import hashlib
import logging
import os
import xdg

def hash_json(j):
    """Hash a JSON object using MD5."""
    j_enc = json.dumps(j).encode("utf-8")
    j_hash = hashlib.md5(j_enc).hexdigest()
    return j_hash


def get_logger(name, debug=False, time=True):
    """Get a logger with the specified name and debug level."""
    logging.addLevelName(logging.CRITICAL, "C")
    logging.addLevelName(logging.ERROR, "E")
    logging.addLevelName(logging.WARNING, "W")
    logging.addLevelName(logging.INFO, "I")
    logging.addLevelName(logging.DEBUG, "D")
    if time:
        fmt = "[%(asctime)13s:%(name)10s:%(levelname)1s:%(funcName)15s] %(message)s"
    else:
        fmt = "[%(name)10s:%(levelname)1s:%(funcName)15s] %(message)s"
    datefmt = "%Y%m%d %H:%M:%S"
    logging.basicConfig(level=logging.INFO, format=fmt, datefmt=datefmt)
    logger = logging.getLogger(name)
    if debug:
        logger.setLevel(logging.DEBUG)
    return logger


class ADef:
    """Apparatus Definitions module."""
    DATA_DIR = f"{xdg.XDG_DATA_HOME}/apparatus"
    CONFIG_DIR = f"{xdg.XDG_CONFIG_HOME}/apparatus"

    def __init__(self, class_name):
        """Initialize the Apparatus Definitions configuration."""
        self.photo_dir = f"{self.DATA_DIR}/{class_name}/photos"
        if not os.path.isdir(self.photo_dir):
            os.makedirs(self.photo_dir)
        self.config_dir = self.CONFIG_DIR
        if not os.path.isdir(self.photo_dir):
            os.makedirs(self.photo_dir)