from time import sleep
import RPi.GPIO as GPIO
import math,random,time
from datetime import datetime
import sqlite3

conn=sqlite3.connect('speedometer.db')
c=conn.cursor()

def create_table():
        c.execute("CREATE TABLE IF NOT EXISTS speedoValues(unix REAL,datestamp TEXT,speed REAL,trip_dist REAL,avg_time REAL)")

def rps(channel):
        global time_interval,counter
        counter+=1
        if len(time_interval)==2:
                time_interval[1]=time_interval[0]
                time_interval[0]=datetime.now()
                #print (time_interval[0]-time_interval[1]).microseconds
        else:
                time_interval.append(datetime.now())

def calculate_speed(r_cm):
        global time_interval
        if len(time_interval)==0 or len(time_interval)==1:
                km_per_hour=0
        else:
                time_diff=time_interval[0]-time_interval[1]
                time_diff=time_diff.microseconds*1.0/(10**6)
                circ_cm = (2 * math.pi) * r_cm
                dist_km = (circ_cm) / 100000.0 # convert to kilometres
                km_per_sec = (dist_km ) / time_diff
                km_per_hour = km_per_sec * 3600 # convert to distance per hour
        return km_per_hour

def calculate_trip_speed(counter,r_cm):
        trip_distance=(2*math.pi*r_cm*counter)
        return trip_distance/100000


create_table()

global kmph
global trip_distance,start_time
GPIO.setmode(GPIO.BOARD)     # set up BCM GPIO numbering

# Set up input pin
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
start_time=0
time_interval=[]
counter=0
# Callback function to run in another thread when button pressed

# add event listener on pin 16
# event will interrupt the program and call the buttonPressed function
GPIO.add_event_detect(16, GPIO.RISING, callback=rps, bouncetime=100)


while True:
        start_time+=1
        sleep(1)
        current_time=datetime.now()
        if len(time_interval)==2 and (current_time-time_interval[0]).seconds>=1:
                #time_interval[0]=current_time
                kmph=0.0
        else:
                kmph=calculate_speed(36.0)
        trip_dist=calculate_trip_speed(counter,36.0)
        avg_time=start_time/60.0
	unix=time.time()
        date=str(current_time.strftime('%Y-%m-%d %H:%M:%S'))
        d = {'speed':kmph,'date':date,'trip_dist':trip_dist,'avg_time':avg_time}
        requests.post('http://127.0.0.1:5000',params = d)
        #c.execute("INSERT INTO speedoValues(unix,datestamp,speed,trip_dist,avg_time) VALUES (?, ?, ?, ?, ?)",(unix,date,kmph,trip_dist,avg_time))
        #conn.commit()
	print "Speed is {} and dist is {}".format(kmph,trip_dist)

c.close()
conn.close()
