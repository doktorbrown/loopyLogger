'''
Created on Apr 22, 2017

@author: doktorbrown
'''

import serial, csv

#from Terminal, cd to directory with this file and run with 'python loopyLogger.py'
#logs approximately every 6 seconds to CSV at about 1MB per hour
#connect to UnidenBCD436HP over USB when scanner is set to serial mode

ser = serial.Serial(
    port='/dev/cu.usbmodem14241',
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1

)



def checkSerial(bcdCommand,ser):
    ser.write(bcdCommand +'\r\n')     # write a string
    statusB= ser.read(4000)
    return statusB + bcdCommand

def csvLogger(cell1,cell2,cell3,cell4,cell5,cell6,csvLogOutput):
    row_to_enter = (cell1,cell2,cell3,cell4,cell5,cell6, '\n')
    csvLogs = csv.writer(open(csvLogOutput, 'a'))
    csvLogs.writerow(row_to_enter)
#     print "logging"
    


def main(ser):
    bcdCommand=('GLG','DTM','STS','GSI','PWR','DTM')
    csvLogOutput = "ScannerLogs.csv"

    
    while True:
        statusGLG = checkSerial(bcdCommand[0],ser)
        statusDTM1 = checkSerial(bcdCommand[1],ser)
        statusSTS = checkSerial(bcdCommand[2],ser)
        statusGSI = checkSerial(bcdCommand[3],ser)
        statusPWR = checkSerial(bcdCommand[4],ser)
        statusDTM2 = checkSerial(bcdCommand[5],ser)

        csvLogger(statusGLG,statusDTM1,statusSTS,statusGSI,statusPWR,statusDTM2,csvLogOutput)
        print statusGLG,statusDTM1
#         print"logged"
    return


if __name__ == '__main__':
    

    pass


main(ser)