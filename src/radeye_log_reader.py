#!/usr/bin/python
import serial
import time
import binascii

def logdata(outfile, data):
    with open(outfile,'ab') as f: # append to the file in byte mode
        f.write(data)  
        f.write("--- next output --- \n")  

if __name__ == "__main__":
    outfile="radeye_bytes.log"
        
    rawdata=''
    with open(outfile,'rb') as f: # append to the file in byte mode
        rawdata=f.read()  
    out=''
    ourString=''
    for rawByte in rawdata:
        out += 'x\\'+str(binascii.hexlify(rawByte)+ " ")
        ourString += rawByte
        if (rawByte == '\n'):
            print(out)
            print(ourString)
            out = ''
            ourString=''
