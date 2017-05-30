'''
Created on May 28, 2017

@author: catawbafellini

Tkinter implementation
'''
'''
Created on Apr 22, 2017

@author: doktorbrown
'''

import serial, csv,os
import Tkinter as tk
# from Tkinter import *
# from Tkinter import Ttk

## from Terminal, cd to directory with this file and run with 'python speedyLogger.py'
## logs approximately every 3 seconds to CSV at about 2MB per hour(vs. 6 seconds 1MB/hr with loopyLogger)

# as of 5.29.17 now logs to /Desktop at about 1.1K/min and out to a Tkinter window.  This has also been turned into standalone app with py2app

#connect to UnidenBCD436HP over USB when scanner is set to serial mode

ser = serial.Serial(
#     port='/dev/cu.usbmodem14241',
    port='/dev/cu.usbmodem14211', 
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

def csvLogger(cell1,cell2,cell3,cell4,cell5,cell6,cell7,cell8,cell9,cell10,csvLogOutput): #add more cells once items parsed in uniD()
    row_to_enter = (cell1,cell2,cell3,cell4,cell5,cell6,cell7,cell8,cell9,cell10, '\n') 
    csvLogs = csv.writer(open(csvLogOutput, 'a'))
    csvLogs.writerow(row_to_enter)
#     print "logging"
    
def newPath(): #find userName to allow saving on OSX
    p = os.path.abspath('test.txt') 
    aa=p.split('/')
#     print 'aa', aa
    userName =  aa[2]  
#     print 'aa-split', aa[2] 
    newPath = '/Users/'+userName+"/Desktop/" 
#     print newPath  
    return newPath 

def uniD(ser):
    bcdCommand=('GLG','DTM','STS','GSI','PWR','DTM')
 
    csvLogOutput = newPath() + "newLog.csv" 

    
    statusGLG = checkSerial(bcdCommand[0],ser)
    statusDTM1 = checkSerial(bcdCommand[1],ser)
    statusGSI = checkSerial(bcdCommand[3],ser)
#     beans= statusGLG,statusDTM1
#     print beans

#     crush the beans    
    dayOfDay = statusDTM1.split(',')
#     print timeOfDay[5]
    dayTimer= dayOfDay[3]+'.'+dayOfDay[4]+'.'+dayOfDay[2]
    print dayTimer
    
    
    timeOfDay = statusDTM1.split(',')
#     print timeOfDay[5]
    shorTimer= timeOfDay[5]+':'+timeOfDay[6]+':'+timeOfDay[7]
    print shorTimer 
    
    channelInfo = statusGLG.split(',')
#     print  channelInfo
#     channelInfoList= 'Frequency:  '+channelInfo[1]+'\n'+'Type:  '+channelInfo[2]+'\n'+'System:  '+channelInfo[5]+'\n'+'Dept:  '+channelInfo[6]+'\n'+'Talk Group:  '+channelInfo[7]+'\n'
#     print channelInfoList
    Frequency=str(channelInfo[1])
    Type=str(channelInfo[2])
    System=str(channelInfo[5])
    Department=str(channelInfo[6])
    TalkGroup=str(channelInfo[7])
    
    
    p25Info = statusGSI.split('<') 
#     print  p25Info
    p25List= 'Frequency:  '+p25Info[5]+'\n'+'Type:  '+p25Info[6]+'\n'+'TGID:  '+p25Info[7]+'\n'+'UnitID:  '+p25Info[8]+'\n'+'Talk Group:  '+p25Info[10]+'\n' 
    print p25List 
    
    try:
        tgID= statusGSI.split('TGID:')  
        tgStr=tgID[1]
        talkg=tgStr.split('"')
        TGID=str(talkg[0])    
    except:
        TGID=str(0)
    print 'TGID: ',TGID  
    
    
    try:
        unitID= statusGSI.split('UID:')  
        unitStr=unitID[1]
        unit=unitStr.split('"')
        UID=str(unit[0])    
    except:
        UID=str(0)
    print 'UID: ',UID  
    
    try:
        Rssi = statusGSI.split('Rssi="')  
#     print  p25Info
        RSSIbegin= Rssi[1]
        RSSIsplit=RSSIbegin.split('"')
        RSSI=str(RSSIsplit[0])
    except: 
        RSSI=str(0)
    print 'RSSI: ',RSSI 
    
#     throw the crushed beans back out as a big mess for now. eventually need to use separate widgets in Tk to display these
#     beans=(dayTimer+
#            '  '+
#            shorTimer+
#            '\n'+'\n'+
#            'Frequency:  '+Frequency+'\n'+
#            'Type:  '+Type+'\n'+
#            'System: '+System+'\n'+
#            'Department:  '+Department+'\n'+
#            'Talk Group:  '+TalkGroup+'\n'+'\n'+
#            'RSSI:  '+RSSI+'\n'+
#            'TGID:  '+TGID+'\n'+
#            'UID:  '+UID
#            )
#         print"logged"
# at least it all goes to CSV in slightly tidier format than the original status msgs    
    csvLogger(dayTimer,shorTimer,Frequency,Type,System,Department,TalkGroup,RSSI,TGID,UID,csvLogOutput)
    beans=(dayTimer,shorTimer,Frequency,Type,System,Department,TalkGroup,RSSI,TGID,UID) 
#     return beans,dayTimer,shorTimer,Frequency,Type,System,Department,TalkGroup,RSSI,TGID,UID
    return beans


def update():
    beans=uniD(ser)
    
#     dayTimer,shorTimer,Frequency,Type,System,Department,TalkGroup,RSSI,TGID,UID
    daY.config(text=beans[0])
    timE.config(text=beans[1])
    freQ.config(text=beans[2])
    typE.config(text=beans[3])
    sysT.config(text=beans[4])
    depT.config(text=beans[5])
    talK.config(text=beans[6])
    rssi.config(text=beans[7])
    tgiD.config(text=beans[8])
    uiD.config(text=beans[9])   
    root.after(100, update)  
 
root = tk.Tk()
root.title("bunco dribble")
# root.toplevel(bg='green')  

daY = tk.Label(text='0',padx=25)    
daY.place(x=25, y=25) 

timE = tk.Label(text='0',padx=55)     
timE.place(x=250, y=25) 

freQ = tk.Label(text='0',padx=25)      
freQ.place(x=25, y=75)

typE = tk.Label(text='0',padx=25)     
typE.place(x=25, y=100)

sysT = tk.Label(text='0',padx=25)      
sysT.place(x=25, y=125)

depT = tk.Label(text='0',padx=25)     
depT.place(x=25, y=150)

talK = tk.Label(text='0',padx=25)     
talK.place(x=25, y=175)

rssi = tk.Label(text='0',padx=25) 
rssi.place(x=600, y=25)     
# rssi.pack()
# rssi.pack(side = "right") 

tgiD = tk.Label(text='0',padx=25)      
tgiD.place(x=25, y=225)

uiD = tk.Label(text='0',padx=25)    
uiD.place(x=25, y=250) 
 

 
root.after(100, update)
root.geometry("800x300+0+0") 
root.mainloop() 

