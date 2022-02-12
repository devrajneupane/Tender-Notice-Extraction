from email import message
from glob import glob
from pathlib import Path
import datetime
import sys
import os
import logging

filename=None
logger=None
count=0
class Logger(object):
    
    def __init__(self,fname=None):
        global filename,logger
        self.path = Path(__file__).parent
        self.stdout = sys.stdout
        sys.stdout=self
        if fname is not None:
            global logger
            try:
                os.mkdir(self.path.parent.joinpath("logs"))
            except FileExistsError:
                pass
            filename=fname.strftime("%Y-%m-%d (%Hh-%Mm-%Ss-%fus)") 
            logging.basicConfig(filename=str(self.path.parent.joinpath("logs","log-"+filename+".txt")),filemode="w+",format='%(asctime)s > %(message)s') 
            logger=logging.getLogger() 
            logger.setLevel(level=logging.INFO)

    def write(self, message):
        global count
        count += 1
        self.stdout.write(message)
        msg=message.replace("\n","")
        count = count-1
        self.fl_write(msg)
        
    def fl_write(self,msg):
        global logger,count
        if count==0 and len(msg)>0:        
            logger.info(msg)
            
    def flush(self):
        pass

# file=None
# class Logger(object):
#     def __init__(self, file_name=None):
#         global filename,file
#         self.path = Path(__file__).parent
#         if file_name is not None:
#             try:
#                 os.mkdir(self.path.parent.joinpath("logs"))
#             except FileExistsError:
#                   pass
#             filename=file_name.strftime("%Y-%m-%d (%Hh-%Mm-%Ss-%fus)")
#             file = open(str(self.path.parent.joinpath("logs","log-"+filename+".txt")), 'w+', encoding="utf-8",)
#         self.stdout = sys.stdout
#         sys.stdout = self
#     def __del__(self):
#         global file
#         sys.stdout = self.stdout
#         file.close()
#     def write(self, data):
#         global file 
#         file.write(data)
#         self.stdout.write(data)
#     def flush(self):
#         global file
#         file.flush()