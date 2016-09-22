#!/bin/sh
#launcher.sh

cd gps
sudo python simplegps.py &
cd ../accgyro
sudo python simpleaccgyro1.py &
cd ../speedometer
sudo python test.py &
