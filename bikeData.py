#speedometer
from time import sleep
import RPi.GPIO as GPIO
import math,random,time
from datetime import datetime
import sqlite3





conn=sqlite3.connect('sensors.db')
c=conn.cursor()

def create_table():
        c.execute("CREATE TABLE IF NOT EXISTS sensorValues(unix REAL,datestamp TEXT,speed REAL,trip_dist REAL,avg_time REAL,cadence REAL)")


#speedometer
def rps(channel):
        global time_interval,counter
        counter+=1
        if len(time_interval)==2:
                time_interval[1]=time_interval[0]
                time_interval[0]=datetime.now()
                #print (time_interval[0]-time_interval[1]).microseconds
        else:
                time_interval.append(datetime.now())

def cadence(channel):
        global cadence_interval
        cadence_counter+=1
        if len(cadence_interval)==2:
                cadence_interval[1]=cadence_interval[0]
                cadence_interval[0]=datetime.now()
                #print (time_interval[0]-time_interval[1]).microseconds
        else:
                cadence_interval.append(datetime.now())

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

def calculate_cadence():
        global cadence_interval
        if len(cadence_interval)==0 or len(cadence_interval)==1:
                rpm=0
        else:
                cadence_diff=cadence_interval[0]-cadence_interval[1]
                cadence_diff=cadence_diff.microseconds*1.0/(10**6)
                rpm = 1 / (cadence_diff * 300)
        return rpm

def calculate_trip_speed(counter,r_cm):
        trip_distance=(2*math.pi*r_cm*counter)
        return trip_distance/100000





#speedometer

global trip_distance,start_time,kmph
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
start_time=0
time_interval=[]
cadence_interval=[]
counter=0
cadence_counter=0
GPIO.add_event_detect(16, GPIO.RISING, callback=rps, bouncetime=100)
GPIO.add_event_detect(18, GPIO.RISING, callback=cadence, bouncetime=100)





create_table()
while True:
        #speedometer
        start_time+=1
        
        current_time=datetime.now()
        if len(time_interval)==2 and (current_time-time_interval[0]).seconds>=1:
                time_interval[0]=current_time
                kmph=0.0
        else:
                kmph=calculate_speed(35.0)

        if len(cadence_interval)==2 and (current_time-cadence_interval[0]).seconds>=1:
                cadence_interval[0]=current_time
                rpm=0.0
        else:
                rpm=calculate_cadence()
                
        trip_dist=calculate_trip_speed(counter,35.0)
        avg_time=start_time/60.0
        
        unix=time.time()
        date=str(current_time.strftime('%Y-%m-%d %H:%M:%S'))

        c.execute("INSERT INTO sensorValues(unix,datestamp,speed,trip_dist,avg_time,cadence) VALUES (?, ?, ?, ?, ?, ? )",(unix,date,kmph,trip_dist,avg_time,rpm))
        conn.commit()
        print(unix,date,kmph,trip_dist,avg_time,rpm)
        print "done"

c.close()
conn.close()        