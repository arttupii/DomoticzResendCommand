import requests
import pprint
import json
import time

url = "http://192.168.100.100:8080"
resendMaxCount=5
resendInterval=60

def getDevices():
    response = requests.get(url+"/json.htm?type=devices&filter=light&used=true&order=Name");
    if(response.ok):
       jData =  json.loads(response.content)
       return jData["result"]
        #for v in t:
        #    print v["ID"]
    else:
      # If response code is not ok (200), print the resulting http error code with description
        response.raise_for_status()

def turnOnOff(idx,switchcmd):
    print url+"/json.htm?type=command&param=switchlight&idx="+idx+"&switchcmd="+switchcmd
    response = requests.get(url+"/json.htm?type=command&param=switchlight&idx="+idx+"&switchcmd="+switchcmd);
    if(response.ok):
       jData =  json.loads(response.content)
       return jData
    else:
        response.raise_for_status()

lastDeviceState = {}
deviceResendCnt = {}
while True:
    devices = getDevices()
    for device in devices:
        idx=device["idx"]
        lastStatus=lastDeviceState.get(idx)
        lastDeviceState[idx]=device["Status"];
        if deviceResendCnt.get(idx)==None or lastStatus!=device["Status"]:
            deviceResendCnt[idx]=resendMaxCount
            
        if device["SubType"]=="AC" and device["SwitchType"]=="On/Off"  and deviceResendCnt[idx]>0:
            print device["idx"],device["Status"],deviceResendCnt[idx]
            turnOnOff(idx, device["Status"]);
            deviceResendCnt[idx]=deviceResendCnt[idx]-1;
    time.sleep(resendInterval)

