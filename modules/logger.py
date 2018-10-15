import datetime
import sys
import logging
import logging.config
import inspect
import json

dConfDefault = {"version": 1,
                "disable_existing_loggers": True,
                "formatters": { "standard": { "format": "%(asctime)s : %(levelname)8s : %(message)s" } },
                "handlers":   { "standard": { "class": "logger.cMyLogHandler", "formatter": "standard", "level": "DEBUG" },
                                "socket":   { "class": "logging.handlers.SocketHandler", "formatter": "standard", "level": "DEBUG", "host": "localhost", "port": 3000 }
                              }
               }

class cMyLogHandler(logging.StreamHandler):

   def __init__(self):
      logging.StreamHandler.__init__(self) # always call base class constructor at the very beginning
      self.sName = self.__class__.__name__
      self.bWithinTune = False
      if ("nu" in sys.modules): # automatic detection if called within Tune
            import nu as NU
            self.nu = NU
            self.bWithinTune = True

   def emit(self, record):
      try:
         msg = self.format(record)
         if self.bWithinTune == True:
            self.nu.log("{}".format(msg))
         else:
            print "{}".format(msg)
      except:
         self.handleError(record)

class cLogger:

   def __init__(self, initConfig = None, bUseTimestamp = True, bWithinTune = False):
      self.sName = self.__class__.__name__
      self.__executeSingleton() # singleton!
      if initConfig != None:
         self.configure(initConfig)

   def configure(self, oConf, bUseDefault=True):
      if isinstance(oConf,dict):
         oDict = oConf
      else:
         oFile = open( oConf, 'r' )
         oDict = json.load(oFile)
         oFile.close()
      if bUseDefault == True:
         oDict.update(dConfDefault)
      logging.config.dictConfig(oDict)
      self.LogDebug(self.sName, "New logger configuration: {}".format(oDict))

   def __executeSingleton(self):
      if not hasattr(logging, "ALWAYS"):
         self.__addNewLoggingLevel('ALWAYS', logging.CRITICAL + 10)

   def __addNewLoggingLevel(self, levelName, levelNum, methodName=None):
      # from https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility
      if not methodName:
         methodName = levelName.lower()

      if hasattr(logging, levelName):
         raise AttributeError('{} already defined in logging module'.format(levelName))
      if hasattr(logging, methodName):
         raise AttributeError('{} already defined in logging module'.format(methodName))
      if hasattr(logging.getLoggerClass(), methodName):
         raise AttributeError('{} already defined in logger class'.format(methodName))

      # This method was inspired by the answers to Stack Overflow post
      # http://stackoverflow.com/q/2183233/2988730, especially
      # http://stackoverflow.com/a/13638084/2988730
      def logForLevel(self, message, *args, **kwargs):
         if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)
      def logToRoot(message, *args, **kwargs):
         logging.log(levelNum, message, *args, **kwargs)

      logging.addLevelName(levelNum, levelName)
      setattr(logging, levelName, levelNum)
      setattr(logging.getLoggerClass(), methodName, logForLevel)
      setattr(logging, methodName, logToRoot)

   def LogDebug(self, sName, sText):
      (sFilename, iLineNum, sFuncName, sExeLines, iIndex) = inspect.getframeinfo(inspect.currentframe().f_back)
      oLogger = logging.getLogger(sName)
      oLogger.debug("{} : {}()#{} : {}".format(sName, sFuncName, iLineNum, sText))

   def LogInfo(self, sName, sText):
      (sFilename, iLineNum, sFuncName, sExeLines, iIndex) = inspect.getframeinfo(inspect.currentframe().f_back)
      oLogger = logging.getLogger(sName)
      oLogger.info("{} : {}()#{} : {}".format(sName, sFuncName, iLineNum, sText))

   def LogWarning(self, sName, sText):
      (sFilename, iLineNum, sFuncName, sExeLines, iIndex) = inspect.getframeinfo(inspect.currentframe().f_back)
      oLogger = logging.getLogger(sName)
      oLogger.warning("{} : {}()#{} : {}".format(sName, sFuncName, iLineNum, sText))

   def LogError(self, sName, sText):
      (sFilename, iLineNum, sFuncName, sExeLines, iIndex) = inspect.getframeinfo(inspect.currentframe().f_back)
      oLogger = logging.getLogger(sName)
      oLogger.error("{} : {}()#{} : {}".format(sName, sFuncName, iLineNum, sText))

   def LogAlways(self, sName, sText):
      (sFilename, iLineNum, sFuncName, sExeLines, iIndex) = inspect.getframeinfo(inspect.currentframe().f_back)
      oLogger = logging.getLogger(sName)
      oLogger.always("{} : {}()#{} : {}".format(sName, sFuncName, iLineNum, sText))

   # Old API. Please do not use anymore
   def loggerDebug(self, bDebug, sName, sText):
      (sFilename, iLineNum, sFuncName, sExeLines, iIndex) = inspect.getframeinfo(inspect.currentframe().f_back)
      oLogger = logging.getLogger(sName)
      oLogger.debug("{} : {}()#{} : {}".format(sName, sFuncName, iLineNum, sText))

