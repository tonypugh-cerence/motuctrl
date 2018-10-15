import sys
import logging
import time

sys.path.append( "modules" )

from motu import cMotuCtrl
from logger import cLogger

dJsonLogger = { "loggers":    { "":               { "handlers":["standard","socket"], "level": "ERROR" }, # Root logger
                                "cMotuCtrl":      { "handlers":["standard","socket"], "level": "ERROR", "propagate": False}}}
myLog = cLogger(dJsonLogger)

sDeviceIpAddress = '192.168.1.100'
oMotu001 = cMotuCtrl(sDeviceIpAddress)

if sys.argv == 0:
	print 'Error : No mixer level value passed in commandline'
else:
	print 'Number of arguments:', len(sys.argv), 'arguments.'
	print 'Argument List:', str(sys.argv)
	fValueDb = float(sys.argv[1])
	
	iMixChannelList = [16, 17, 18]
	for iMixChannel in iMixChannelList:
		oMotu001.setMixerInFaderDb(iMixChannel, fValueDb)
		fValueDbDev = oMotu001.getMixerInFaderDb(iMixChannel)
		if fValueDbDev:
			print "Set Mixer Fader Ch {}: Request {:4.2f} dB | Set on device {:4.2f} dB".format(iMixChannel, fValueDb, fValueDbDev)


