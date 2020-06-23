import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
#Provide your IBM Watson Device Credentials
organization = "jfxbyq"
deviceType = "RASPBERRYPI"
deviceId = "654321"
authMethod = "token"
authToken = "12345678"

# Initialize GPIO

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)
        print(type(cmd.data))
        i=cmd.data['command']
        if i=='lighton':
                print("light is on")
        elif i=='lightoff':
                print("light is off")

try:
        deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
        deviceCli = ibmiotf.device.Client(deviceOptions)#.............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        
        temp= 101
        #print(temp)
        bp = random.randint(80,120)
        #Send Temperature, Bloodpressure & Pulse to IBM Watson
        pul = random.randint(60,100)
        data = { 'Temperature' : temp, 'Bloodpressure': bp, 'Pulse':pul }
        #print (data)
        def myOnPublishCallback():
            print ("Published Temperature = %s F" % temp, "Bloodpressure = %s " % bp, "Pulse = %s " % pul, "to IBM Watson")

        success = deviceCli.publishEvent("DHT11", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
