#!/usr/bin/python
""" Serial communication for the Thermo Scientific RadEye GN+ radiation detector.
    - Writes output to a log file
"""


import serial
import time

def logdata(outfile, data):
    with open(outfile,'ab') as f: # append to the file in byte mode
        f.write(data)  
        f.write("--- next output --- \n")  

if __name__ == "__main__":
    logfile="radeye_bytesSim.log"
    
    # Establish a serial port connection IAW specification on page 2-1
    controlBytes=['\x02','\x03']
    ser = serial.Serial(
        # port='/dev/ttyUSB0',
        port='/dev/ttyACM0',
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
    byte = ser.read(1)
    logdata(logfile, byte)  
      
    # time.sleep(5/10000000) #This line and two above are needed to alert the device that a control command is coming.
    time.sleep(0.5)
    cmd='X1\r\n' # This is the command to make the device start streaming sensor values
    ser.write(cmd)
    byte = ser.read(1)
    logdata(logfile, byte) 
    time.sleep(.01)

    # Start the big while loop
    while True:

        # Collecting data from the Radeye
        out = ''
        while ser.inWaiting() > 0: # While there is a byte in the buffer waiting to be read.
            byte = ser.read() # Read one byte at a time. Readline was not a good solution as it included control bytes.
            if (byte not in controlBytes): # this prevents control bytes from being added to the output.
                out += byte

        logdata(logfile, out)            
        out=out.split(' ')
        print(len(out), out)
        

        time.sleep(0.5)
        
       
