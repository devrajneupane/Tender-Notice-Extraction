from pathlib import Path
import datetime
import sys
import os
import logging

filename=None
logger=None

class Logger(object):
    
    def __init__(self,fname=None):
        global filename,logger
        self.path = Path(__file__).parent
        self.terminal = sys.stdout
        if fname is not None:
            print("hello")
            filename=fname  
            logging.basicConfig(filename=str(self.path.parent.joinpath("logs","log-"+filename+".txt")),filemode="w+",format='%(asctime)s %(message)s') 
            logger=logging.getLogger() 
            logger.setLevel(level=logging.INFO)

    def write(self, message):
        global logger
        self.terminal.write(message)
        if not message == "\n":
            logger.info(message)
            
    def flush(self):
        pass