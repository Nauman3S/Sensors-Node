
import sys
import time
from DFRobot_BMX160 import BMX160

bmx160 = BMX160(1)

#begin return True if succeed, otherwise return False
retryCount=0
while not bmx160.begin():
    retryCount=retryCount+1
    time.sleep(1)
    if(retryCount>=6):
        print('BMX160 Not found. Please check the connections')
        break

def getAccelGyroMag_BMX160():
    global bmx160
    if(retryCount<5):
        data= bmx160.get_all_data()
        payload=str(data[6])+','+str(data[7])+','+str(data[8])+','+str(data[3])+','+str(data[4])+','+str(data[5])+','+str(data[0])+','+str(data[1])+','+str(data[2])+','
        return payload
    else:
        return "0,0,0,0,0,0,0,0,0"