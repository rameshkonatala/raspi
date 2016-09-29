
#speedometer
from time import sleep
import RPi.GPIO as GPIO
import math,random,time
from datetime import datetime
import sqlite3

#gps
import serial
import pynmea2

#accgyro
import smbus
import math,time



conn=sqlite3.connect('sensors.db')
c=conn.cursor()

def create_table():
        c.execute("CREATE TABLE IF NOT EXISTS sensorValues(unix REAL,datestamp TEXT,speed REAL,trip_dist REAL,avg_time REAL,latitude REAL,longitude REAL,temperature REAL,accX REAL,accY REAL,accZ REAL,roll REAL,pitch REAL)")





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



#accgyro
class MPU6050:

    # Global Variables
    GRAVITIY_MS2 = 9.80665
    address = None
    bus = smbus.SMBus(1)

    # Scale Modifiers
    ACCEL_SCALE_MODIFIER_2G = 16384.0
    ACCEL_SCALE_MODIFIER_4G = 8192.0
    ACCEL_SCALE_MODIFIER_8G = 4096.0
    ACCEL_SCALE_MODIFIER_16G = 2048.0

    GYRO_SCALE_MODIFIER_250DEG = 131.0
    GYRO_SCALE_MODIFIER_500DEG = 65.5
    GYRO_SCALE_MODIFIER_1000DEG = 32.8
    GYRO_SCALE_MODIFIER_2000DEG = 16.4

    # Pre-defined ranges
    ACCEL_RANGE_2G = 0x00
    ACCEL_RANGE_4G = 0x08
    ACCEL_RANGE_8G = 0x10
    ACCEL_RANGE_16G = 0x18

    GYRO_RANGE_250DEG = 0x00
    GYRO_RANGE_500DEG = 0x08
    GYRO_RANGE_1000DEG = 0x10
    GYRO_RANGE_2000DEG = 0x18

    # MPU-6050 Registers
    PWR_MGMT_1 = 0x6B
    PWR_MGMT_2 = 0x6C

    SELF_TEST_X = 0x0D
    SELF_TEST_Y = 0x0E
    SELF_TEST_Z = 0x0F
    SELF_TEST_A = 0x10

    ACCEL_XOUT0 = 0x3B
    ACCEL_XOUT1 = 0x3C
    ACCEL_YOUT0 = 0x3D
    ACCEL_YOUT1 = 0x3E
    ACCEL_ZOUT0 = 0x3F
    ACCEL_ZOUT1 = 0x40

    TEMP_OUT0 = 0x41
    TEMP_OUT1 = 0x42

    GYRO_XOUT0 = 0x43
    GYRO_XOUT1 = 0x44
    GYRO_YOUT0 = 0x45
    GYRO_YOUT1 = 0x46
    GYRO_ZOUT0 = 0x47
    GYRO_ZOUT1 = 0x48

    ACCEL_CONFIG = 0x1C
    GYRO_CONFIG = 0x1B

    def __init__(self, address):
        self.address = address

        # Wake up the MPU-6050 since it starts in sleep mode
        self.bus.write_byte_data(self.address, self.PWR_MGMT_1, 0x00)

    # I2C communication methods

    def read_i2c_word(self, register):
        """Read two i2c registers and combine them.

        register -- the first register to read from.
        Returns the combined read results.
        """
        # Read the data from the registers
        high = self.bus.read_byte_data(self.address, register)
        low = self.bus.read_byte_data(self.address, register + 1)

        value = (high << 8) + low

        if (value >= 0x8000):
            return -((65535 - value) + 1)
        else:
            return value

    # MPU-6050 Methods

    def get_temp(self):
        """Reads the temperature from the onboard temperature sensor of the MPU-6050.

        Returns the temperature in degrees Celcius.
        """
        raw_temp = self.read_i2c_word(self.TEMP_OUT0)

        # Get the actual temperature using the formule given in the
        # MPU-6050 Register Map and Descriptions revision 4.2, page 30
        actual_temp = (raw_temp / 340.0) + 36.53

        return actual_temp

    def set_accel_range(self, accel_range):
        """Sets the range of the accelerometer to range.

        accel_range -- the range to set the accelerometer to. Using a
        pre-defined range is advised.
        """
        # First change it to 0x00 to make sure we write the correct value later
        self.bus.write_byte_data(self.address, self.ACCEL_CONFIG, 0x00)

        # Write the new range to the ACCEL_CONFIG register
        self.bus.write_byte_data(self.address, self.ACCEL_CONFIG, accel_range)

    def read_accel_range(self, raw = True):
        """Reads the range the accelerometer is set to.

        If raw is True, it will return the raw value from the ACCEL_CONFIG
        register
        If raw is False, it will return an integer: -1, 2, 4, 8 or 16. When it
        returns -1 something went wrong.
        """
        raw_data = self.bus.read_byte_data(self.address, self.ACCEL_CONFIG)

        if raw is True:
            return raw_data
        elif raw is False:
            if raw_data == self.ACCEL_RANGE_2G:
                return 2
            elif raw_data == self.ACCEL_RANGE_4G:
                return 4
            elif raw_data == self.ACCEL_RANGE_8G:
                return 8
            elif raw_data == self.ACCEL_RANGE_16G:
                return 16
            else:
                return -1

    def get_accel_data(self, g = False):
        """Gets and returns the X, Y and Z values from the accelerometer.

        If g is True, it will return the data in g
        If g is False, it will return the data in m/s^2
        Returns a dictionary with the measurement results.
        """
        x = self.read_i2c_word(self.ACCEL_XOUT0)
        y = self.read_i2c_word(self.ACCEL_YOUT0)
        z = self.read_i2c_word(self.ACCEL_ZOUT0)

        accel_scale_modifier = None
        accel_range = self.read_accel_range(True)

        if accel_range == self.ACCEL_RANGE_2G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G
        elif accel_range == self.ACCEL_RANGE_4G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_4G
        elif accel_range == self.ACCEL_RANGE_8G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_8G
        elif accel_range == self.ACCEL_RANGE_16G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_16G
        else:
            print("Unkown range - accel_scale_modifier set to self.ACCEL_SCALE_MODIFIER_2G")
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G

        x = x / accel_scale_modifier
        y = y / accel_scale_modifier
        z = z / accel_scale_modifier

        if g is True:
            return {'x': x, 'y': y, 'z': z}
        elif g is False:
            x = x * self.GRAVITIY_MS2
            y = y * self.GRAVITIY_MS2
            z = z * self.GRAVITIY_MS2
            return {'x': x, 'y': y, 'z': z}

    def set_gyro_range(self, gyro_range):
        """Sets the range of the gyroscope to range.

        gyro_range -- the range to set the gyroscope to. Using a pre-defined
        range is advised.
        """
        # First change it to 0x00 to make sure we write the correct value later
        self.bus.write_byte_data(self.address, self.GYRO_CONFIG, 0x00)

        # Write the new range to the ACCEL_CONFIG register
        self.bus.write_byte_data(self.address, self.GYRO_CONFIG, gyro_range)

    def read_gyro_range(self, raw = False):
        """Reads the range the gyroscope is set to.

        If raw is True, it will return the raw value from the GYRO_CONFIG
        register.
        If raw is False, it will return 250, 500, 1000, 2000 or -1. If the
        returned value is equal to -1 something went wrong.
        """
        raw_data = self.bus.read_byte_data(self.address, self.GYRO_CONFIG)

        if raw is True:
            return raw_data
        elif raw is False:
            if raw_data == self.GYRO_RANGE_250DEG:
                return 250
            elif raw_data == self.GYRO_RANGE_500DEG:
                return 500
            elif raw_data == self.GYRO_RANGE_1000DEG:
                return 1000
            elif raw_data == self.GYRO_RANGE_2000DEG:
                return 2000
            else:
                return -1

    def get_gyro_data(self):
        """Gets and returns the X, Y and Z values from the gyroscope.

        Returns the read values in a dictionary.
        """
        x = self.read_i2c_word(self.GYRO_XOUT0)
        y = self.read_i2c_word(self.GYRO_YOUT0)
        z = self.read_i2c_word(self.GYRO_ZOUT0)

        gyro_scale_modifier = None
        gyro_range = self.read_gyro_range(True)

        if gyro_range == self.GYRO_RANGE_250DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG
        elif gyro_range == self.GYRO_RANGE_500DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_500DEG
        elif gyro_range == self.GYRO_RANGE_1000DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_1000DEG
        elif gyro_range == self.GYRO_RANGE_2000DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_2000DEG
        else:
            print("Unkown range - gyro_scale_modifier set to self.GYRO_SCALE_MODIFIER_250DEG")
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG

        x = x / gyro_scale_modifier
        y = y / gyro_scale_modifier
        z = z / gyro_scale_modifier

        return {'x': x, 'y': y, 'z': z}

    def get_all_data(self):
        """Reads and returns all the available data."""
        temp = get_temp()
        accel = get_accel_data()
        gyro = get_gyro_data()

        return [accel, gyro, temp]




#speedometer
global kmph
global trip_distance,start_time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
start_time=0
time_interval=[]
counter=0
GPIO.add_event_detect(16, GPIO.RISING, callback=rps, bouncetime=100)



#gps
<<<<<<< HEAD
serialStream = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)
=======
serialStream = serial.Serial("/dev/ttyAMA0", 9600,timeout=0.5)
>>>>>>> c89021b43549ccb14ff5b58f84de914b940172ce



create_table()
while True:
        

        #speedometer
        start_time+=1
        
        current_time=datetime.now()
        if len(time_interval)==2 and (current_time-time_interval[0]).seconds>=1:
                time_interval[0]=current_time
                kmph=0.0
        else:
                kmph=calculate_speed(36.0)
        trip_dist=calculate_trip_speed(counter,36.0)
        avg_time=start_time/60.0
	
        unix=time.time()
        date=str(current_time.strftime('%Y-%m-%d %H:%M:%S'))

        #gps
        sentence = serialStream.readline()
<<<<<<< HEAD
        if sentence.find('GGA') > 0:
                data = pynmea2.parse(sentence)
                lat=data.latitude
                lon=data.longitude

        #accgyro
                mpu = MPU6050(0x68)
                temp=mpu.get_temp()
                accel_data = mpu.get_accel_data()
                accX=(accel_data['x'])
                accY=(accel_data['y'])
                accZ=(accel_data['z'])
                gyro_data = mpu.get_gyro_data()
                #print(gyro_data['x'])
                #print(gyro_data['y'])
                #print(gyro_data['z'])
                ax=accel_data['x']
                ay=accel_data['y']
                az=accel_data['z']
                roll  = (math.atan2(ay, math.sqrt((ax*ax) + (az*az)))*180.0)/math.pi;
                pitch = (math.atan2(ax, math.sqrt((ay*ay) + (az*az)))*180.0)/math.pi;
                

                c.execute("INSERT INTO sensorValues(unix,datestamp,speed,trip_dist,avg_time,latitude,longitude,temperature,accX,accY,accZ,roll,pitch) VALUES (?, ?, ?, ?, ? ,? ,? ,? ,? ,? ,? ,? ,? )",(unix,date,kmph,trip_dist,avg_time,lat,lon,temp,accX,accY,accZ,roll,pitch))
                conn.commit()
              
                print "done"

c.close()
conn.close()
=======
        if sentence.find('GGA')>0:
		data = pynmea2.parse(sentence)
	
        lat=data.latitude
        lon=data.longitude
        
        #accgyro
        mpu = MPU6050(0x68)
        temp=mpu.get_temp()
        accel_data = mpu.get_accel_data()
        accX=(accel_data['x'])
        accY=(accel_data['y'])
        accZ=(accel_data['z'])
        gyro_data = mpu.get_gyro_data()
        #print(gyro_data['x'])
        #print(gyro_data['y'])
        #print(gyro_data['z'])
        ax=accel_data['x']
        ay=accel_data['y']
        az=accel_data['z']
        roll  = (math.atan2(ay, math.sqrt((ax*ax) + (az*az)))*180.0)/math.pi;
        pitch = (math.atan2(ax, math.sqrt((ay*ay) + (az*az)))*180.0)/math.pi;
        

        c.execute("INSERT INTO sensorValues(unix,datestamp,speed,trip_dist,avg_time,latitude,longitude,temperature,accX,accY,accZ,roll,pitch) VALUES (?, ?, ?, ?, ? ,? ,? ,? ,? ,? ,? ,? ,? )",(unix,date,kmph,trip_dist,avg_time,lat,lon,temp,accX,accY,accZ,roll,pitch))
        conn.commit()
        print "done"

c.close()
conn.close()

>>>>>>> c89021b43549ccb14ff5b58f84de914b940172ce
