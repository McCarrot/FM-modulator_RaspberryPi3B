#!/usr/bin/python2

from time import sleep
import csv
from Adafruit_Si4713 import Adafruit_Si4713

FMSTATION = 10100
POWER = 88

def readstation():
	with open('scan.csv') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		next(reader)				# Now reading the "header" of the CSV file
		lis = next(reader)			# Now reading the first line of actual data
		fmstation = float(lis[1])	# Convert detected peak to a float
		fmstation = fmstation * 100	# Convert to a multiple of 10kHz
		fmstation = int(fmstation)	# Convert to int
		temp = fmstation % 5
		if temp < 3:				# Round frequency up or down to nearest multiple of 50kHz
			fmstation = fmstation - temp
		else:
			fmstation = fmstation + (5-temp)
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

	radio.readTuneMeasure(FMSTATION)
	printInfo()

	radio.setTXpower(POWER)
	radio.tuneFM(FMSTATION)

	radio.beginRDS()
	radio.setRDSstation("- Inline DAB -")
	radio.setRDSbuffer(" -- empty -- ")

	while True:
		FMSTATION_NEW = int(readstation())
		if FMSTATION != FMSTATION_NEW:
			FMSTATION = FMSTATION_NEW
			radio.tuneFM(FMSTATION)
			radio.setRDSstation("- Inline DAB -")
		printInfo()

		sleep(3)

		# radio.setRDSstation("Galaxy")
		# sleep(5)

		# radio.setRDSstation("News")
		# sleep(5)

		# radio.setRDSstation("Radio")
		# sleep(5)

