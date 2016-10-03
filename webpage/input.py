import requests,time,datetime


for x in xrange(0,100):
	speed = x+100;
	current_time=datetime.datetime.now()
	date=str(current_time.strftime('%H : %M : %S'))
	d = {'speed':speed,'time':date,'trip_dist':speed*3,'trip_time':speed*4}
	requests.post('http://127.0.0.1:5000',params = d)
	time.sleep(0.5)
