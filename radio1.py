#!/usr/bin/python2

from time import sleep
from Adafruit_Si4713 import Adafruit_Si4713
import csv

FMSTATION = 10100
POWER = 90

def readstation():
	file = open("radioconfig.txt")
	fmstation = file.readline()
	file.close()
	return fmstation

def printInfo():
	radio.readASQ()
	print "ASQ:", hex(radio.currASQ), "- InLevel:", radio.currInLevel, "dBfs -",
	radio.readTuneStatus()
	print "Power:", radio.currdBuV, "dBuV - ANTcap:", radio.currAntCap, "- Noise level:", radio.currNoiseLevel

radio = Adafruit_Si4713()

if not radio.begin():
	print "error! couldn't begin!"

else:
	FMSTATION = readstation()
	FMSTATION = int(FMSTATION)

	radio.readTuneMeasure(FMSTATION)
	printInfo()

	radio.setTXpower(POWER)
	radio.tuneFM(FMSTATION)

	radio.beginRDS()
	radio.setRDSbuffer(" -- empty -- ")

	while True:
		FMSTATION_NEW = int(readstation())
		if FMSTATION != FMSTATION_NEW:
			FMSTATION = FMSTATION_NEW
			radio.tuneFM(FMSTATION)
			radio.setRDSstation("- GNR -")
		printInfo()

		sleep(3)

		# radio.setRDSstation("Galaxy")
		# sleep(5)

		# radio.setRDSstation("News")
		# sleep(5)

		# radio.setRDSstation("Radio")
		# sleep(5)