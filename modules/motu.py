import pycurl
from StringIO import StringIO
from urllib import urlencode

import json
import math

from logger import cLogger

class cMotuCtrl(cLogger):

   def __init__(self, sDeviceIpAddress, iTimeOutSeconds=1):
      cLogger.__init__(self)
      self.sName = self.__class__.__name__
      #
      self.sDeviceIpAddress = sDeviceIpAddress
      self.iConnectionTimeout = iTimeOutSeconds
      self.iTimeout = iTimeOutSeconds

   def getMixerInFader(self, iCh):
      sUrl = 'http://{}/datastore/mix/chan/{}/matrix/fader'.format(self.sDeviceIpAddress, iCh) # Get the mixer fader of channel 0
      oBuffer = StringIO()
      oCurl = pycurl.Curl()
      #oCurl.setopt(oCurl.VERBOSE, True)
      oCurl.setopt(oCurl.URL, sUrl)
      oCurl.setopt(oCurl.CONNECTTIMEOUT, self.iConnectionTimeout)
      oCurl.setopt(oCurl.TIMEOUT, self.iTimeout)
      oCurl.setopt(oCurl.WRITEDATA, oBuffer)
      try:
         oCurl.perform()
      except Exception as e:
         self.LogError( self.sName, "Curl Exception: {}".format(e) )
         return None
      oCurl.close()
      oDecoded = json.loads(oBuffer.getvalue())
      return oDecoded['value']

   def getMixerInFaderDb(self, iCh):
      fValue = self.getMixerInFader(iCh)
      if fValue:
         return 20.0*math.log10(fValue)

   def setMixerInFader(self, iCh, fValue):
      sUrl = 'http://{}/datastore/mix/chan/{}/matrix/fader'.format(self.sDeviceIpAddress, iCh) # Get the mixer fader of channel 0
      sJson = json.dumps({"value":fValue})
      sData = {'json': sJson}
      oCurl = pycurl.Curl()
      #oCurl.setopt(oCurl.VERBOSE, True)
      oCurl.setopt(oCurl.URL, sUrl)
      oCurl.setopt(oCurl.CONNECTTIMEOUT, self.iConnectionTimeout)
      oCurl.setopt(oCurl.TIMEOUT, self.iTimeout)
      oCurl.setopt(oCurl.CUSTOMREQUEST, 'PATCH')
      sDataEnc = urlencode(sData)
      oCurl.setopt(oCurl.POSTFIELDS, sDataEnc)
      try:
         oCurl.perform()
      except Exception as e:
         self.LogError( self.sName, "Curl Exception: {}".format(e) )
         return None
      oCurl.close()

   def setMixerInFaderDb(self, iCh, fValueDb):
      fValue = math.pow(10.0, (fValueDb/20.0))
      self.setMixerInFader(iCh, fValue)

