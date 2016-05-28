import serial
import pynmea2

serialStream = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)

while True:
    sentence = serialStream.readline()
    if sentence.find('GGA') > 0:
        data = pynmea2.parse(sentence)
        print "{time}: {lat},{lon}".format(time=data.timestamp,lat=data.latitude,lon=data.longitude)
