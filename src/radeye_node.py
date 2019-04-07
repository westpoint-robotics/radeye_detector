#!/usr/bin/python
""" Serial communication for the Thermo Scientific RadEye GN+ radiation detector
    - publishes readings as a ROS node
"""

import serial
import rospy
import time

from geometry_msgs.msg import PointStamped


# Sending a serial command to RadEye
# if the return value is length 0, then serial communication timed out.
# TODO: This function is unused and needs further testing
def sendCommand(cmd):
    out = ''
    ser.write('00')
    ser.read(1)
    # time.sleep(5/10000000)
    time.sleep(0.75)
    ser.write(cmd)
    time.sleep(0.75)
    while ser.inWaiting() > 0:
        out += ser.read(1)
        time.sleep(.02)
    return out

if __name__ == "__main__":
    rospy.init_node('radeyeNode', anonymous=True)
    pub = rospy.Publisher('/radiation', PointStamped, queue_size = 1)
    msg = PointStamped()
    
    # Establish a serial port connection IAW specification on page 2-1
    controlBytes=['\x02','\x03']
    ser = serial.Serial(
        # port='/dev/ttyUSB0',
        port='/dev/radeye',
        baudrate=9600,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS,
        xonxoff=False,
        rtscts=False,
        dsrdtr=True
    )
    
    # if the connection was left open, then close it.
    if (ser.isOpen()):
        ser.close()
    # Open the serial connection
    ser.open()
  
    time.sleep(1.5)
    # Send the commands for the device to repeateadly send values every second.
    ser.write('00')
    ser.read(1)
    # time.sleep(5/10000000) #This line and two above are needed to alert the device that a control command is coming.
    time.sleep(0.5)
    cmd='X1\r\n' # This is the command to make the device start streaming sensor values
    ser.write(cmd)
    time.sleep(.01)

    # Start the big while loop
    rate = rospy.Rate(1) #The radeye takes 1 second to udate
    while not rospy.is_shutdown():

        # Collecting data from the Radeye
        out = ''
        while ser.inWaiting() > 0: # While there is a byte in the buffer waiting to be read.
            byte = ser.read() # Read one byte at a time. Readline was not a good solution as it included control bytes.
            if (byte not in controlBytes): # this prevents control bytes from being added to the output.
                out += byte

        out=out.split(' ')
        #print(len(out), out)
        if len(out) >= 7:
            if out[6] == "PRDER":
                msg.point.x = float(out[3])
                msg.point.y = 1  #for PRDER
            else:
                msg.point.x = float(out[1])
                msg.point.y = 0 #for GN+
        else:
            print("msg to short it is less then 7 bytes")

        msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "radeye"
        pub.publish(msg)

        rate.sleep()
        
       
