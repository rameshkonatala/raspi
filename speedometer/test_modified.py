
import RPi.GPIO as GPIO
import math,random,time
from datetime import datetime
import sqlite3

global counter,counter_inst
counter=0
counter_inst=0
start_time=datetime.now()

conn=sqlite3.connect('speedometer.db')
c=conn.cursor()

def create_table():
        c.execute("CREATE TABLE IF NOT EXISTS speedoValues(unix REAL,datestamp TEXT,speed REAL,trip_dist REAL,avg_time REAL)")

def rps(channel):
        counter+=1

def calculate_speed(rps):
        km_per_hour = (2 * math.pi * 36 * rps * 36.0 ) / 1000.0 
        return km_per_hour

def calculate_trip_speed(counter):
        trip_distance=(2*math.pi*36*counter)
        return trip_distance/100000

create_table()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(16, GPIO.RISING, callback=rps, bouncetime=100)


while True:
        rps=counter - counter_inst
        counter_inst=counter
        kmph=calculate_speed(rps)
        trip_dist=calculate_trip_speed(counter)
        current_time=datetime.now()
        avg_time=current_time-start_time
        unix=time.time()
        date=str(current_time.strftime('%Y-%m-%d %H:%M:%S'))
        c.execute("INSERT INTO speedoValues(unix,datestamp,speed,trip_dist,avg_time) VALUES (?, ?, ?, ?, ?)",(unix,date,kmph,trip_dist,avg_time))
        
        conn.commit()
        time.sleep(1)


c.close()
conn.close()