from time import sleep
import RPi.GPIO as GPIO
import math
from datetime import datetime

GPIO.setmode(GPIO.BOARD)     # set up BCM GPIO numbering

# Set up input pin
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

start_time=0
time_interval=[]
counter=0
# Callback function to run in another thread when button pressed
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
# add event listener on pin 16
# event will interrupt the program and call the buttonPressed function
GPIO.add_event_detect(16, GPIO.RISING, callback=rps, bouncetime=100)


while True:
	start_time+=1
	sleep(1)
	current_time=datetime.now()
	if len(time_interval)==2 and (current_time-time_interval[0]).seconds>=1:
		time_interval[0]=current_time
		print (0.0,"kph")
	else:
		print (calculate_speed(36.0), "kph")
	trip_dist=calculate_trip_speed(counter,36.0)
	print trip_dist,"avg distance"
	print start_time/60.0,"avg time"
