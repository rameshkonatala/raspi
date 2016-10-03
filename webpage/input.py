import requests,time

for x in xrange(0,100):
	speed = x+100;
	d = {'speed':speed,'time':speed/2,'trip_dist':speed*3,'trip_time':speed*4}
	requests.post('http://127.0.0.1:5000',params = d)
	time.sleep(0.5)
