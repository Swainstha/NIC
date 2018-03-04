from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

import argparse
parser =  argparse.ArgumentParser(description = 'Commands vehicle')
parser.add_argument('--connect', help="SITl starts if no argument")
args = parser.parse_args()

connection_string = args.connect
sitl = None

if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

print 'Connecting to vehicle on %s'% connection_string
vehicle = connect(connection_string, wait_ready = True, baud = 921600)

print " EKF ok?: %s" % vehicle.ekf_ok
def arm_and_takeoff(aTargetAltitude):
    print "basic pre-arm checks"
    while not vehicle.is_armable:
        print "Waiting for vehicle to initialize"
        print vehicle.rangefinder.distance
        print vehicle.gps_0
        time.sleep(1)
    time.sleep(5)
    print "Arming motors"

    #copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while vehicle.mode.name != "GUIDED":
        print vehicle.mode
        vehicle.mode = VehicleMode("GUIDED")

    while not vehicle.armed:
        print "Waiting for arming ", vehicle.mode.name
        vehicle.armed = True
        time.sleep(1)
    time.sleep(2)    
    print "Taking off!"

    while not vehicle.simple_takeoff(aTargetAltitude):
        if vehicle.location.global_relative_frame.alt > 0.08:
            break
        print vehicle.location.global_relative_frame.alt,"  ",vehicle.armed    
        time.sleep(1)

    while True:
        print "Altitude:", vehicle.location.global_relative_frame.alt
        print "Height :",vehicle.rangefinder.distance
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.90:
            print "Reached target altitude"
            break
        time.sleep(1)

arm_and_takeoff(5)
time.sleep(10)

print "Returning to launch"
vehicle.mode = VehicleMode("LAND")
while vehicle.mode.name != "LAND":
    print vehicle.mode.name
    vehicle.mode = VehicleMode("LAND")

print "mode changed to rtl" 
while True:
    if vehicle.location.global_relative_frame.alt < 0.10:
        break
    print "height :", vehicle.location.global_relative_frame.alt
print "vehicle has landed"
time.sleep(10)
arm_and_takeoff(5)
time.sleep(10)
print "Returning to launch"
vehicle.mode = VehicleMode("LAND")
while vehicle.mode.name != "LAND":
    print vehicle.mode.name
    vehicle.mode = VehicleMode("LAND")

while True:
    if vehicle.location.global_relative_frame.alt < 0.10:
        break
    print "height :", vehicle.location.global_relative_frame.alt


print "Close vehicle object"
vehicle.close()

if sitl is not None:
    sitl.stop()


