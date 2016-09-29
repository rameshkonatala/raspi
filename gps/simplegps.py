import serial
import pynmea2
import sqlite3,time
from datetime import datetime

serialStream = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)

conn=sqlite3.connect('gps.db')
c=conn.cursor()

def create_table():
        c.execute("CREATE TABLE IF NOT EXISTS gpsValues(unix REAL,datestamp TEXT,lat REAL,lon REAL)")

create_table()


while True:
    sentence = serialStream.readline()
    if sentence.find('GGA') > 0:
        data = pynmea2.parse(sentence)
        lat=data.latitude
        lon=data.longitude
        current_time=datetime.now()
        unix=time.time()
        date=str(current_time.strftime('%Y-%m-%d %H:%M:%S'))
        c.execute("INSERT INTO gpsValues(unix,datestamp,lat,lon) VALUES (?, ?, ?, ?)",(unix,date,lat,lon))
        conn.commit()

c.close()
conn.close()