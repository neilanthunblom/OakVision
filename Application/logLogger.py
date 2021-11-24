import logging
import os
import datetime
from definitions import ROOT_DIR

def writeToLog(className, line):
    cwd = os.getcwd()
    os.chdir(ROOT_DIR + "/logs")
    try:
        log = open(className + ".log", "a")
        log.write(line + " at " + str(datetime.datetime.now()) + "\n")
        log.close()
        os.chdir(cwd)
    except:
        with open(os.path.join(path, file), 'w') as fp:
            pass
