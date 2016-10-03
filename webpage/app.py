from flask import Flask,request, render_template

app = Flask(__name__)

speed = 0
distance = 0
time = 0
distance = 0 
trip_time = 0
@app.route('/',methods=['POST'])
def getdata():
	global speed
	global time
	global distance
	global trip_time
	speed = request.args.get('speed')
	time = request.args.get('time')
	distance = request.args.get('trip_dist')
	trip_time = request.args.get('trip_time')
	print "distance : "+str(distance)
	print speed
	print time
	return speed
@app.route("/spd",methods=['GET'])
def speedget():
	print speed
	return str(speed)

@app.route("/time",methods=['GET'])
def timeget():
	print time
	return str(time)
@app.route("/trip_dist",methods=['GET'])
def distget():
	print "dist" + str(distance)
	return str(distance)

@app.route("/trip_time",methods=['GET'])
def triptimeget():
	print "trip_time" + str(trip_time)
	return str(trip_time)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

