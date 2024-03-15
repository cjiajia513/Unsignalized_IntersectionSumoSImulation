import logging
from logging.handlers import RotatingFileHandler
import cpm_cfg as conf
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = BASE_DIR.replace("\\", '/')

def singleton(cls):
    instances = {}
    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance

@singleton
class Cpmlog():
    def __init__(self, name='cpm', level='info', logfile_dir='logs') -> None:
        self.logname = name
        self.log_level = logging.INFO if level.lower() == 'info' else logging.DEBUG
        self.logfile_path = BASE_DIR + '/' + logfile_dir + '/' + self.logname + '.log'
        
        os.makedirs(os.path.dirname(self.logfile_path), exist_ok=True)
       
        
        
    def get_logger(self):
        log_formatter = logging.Formatter(
                '%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
        logFile = self.logfile_path
        log_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024,
                                            backupCount=1, encoding=None, delay=0)
        log_handler.setFormatter(log_formatter)
      
        self.logger = logging.getLogger(self.logname)
        self.logger.setLevel(self.log_level)
        self.logger.addHandler(log_handler)
        return self.logger
