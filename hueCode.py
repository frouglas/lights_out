# -*- coding: utf-8 -*-
"""
Created on Tue Nov 07 18:17:21 2017

@author: doug
"""

import phue as ph
import requests
import xml.etree.ElementTree as ET
import xmlParser as xp
import time

hueIP = '192.168.0.15'
trigger = 1
    

bridge = ph.Bridge(hueIP)

allInfo = bridge.get_api()

lights = bridge.get_light_objects('id')

warnOn = {'transitiontime': 1, 'on': True, 'bri': 254, 'hue': 0, 'sat': 254} 
warnOff = {'transitiontime': 1, 'on': False} 

startHue = lights[6].hue
startBri = lights[6].brightness
startSat = lights[6].saturation
reset = {'transitiontime': 1, 'on': True, 'bri': startBri, 'hue': startHue, 
         'sat': startSat}
currState = {}

r = requests.get(url = 
                 "http://webservices.nextbus.com/service/publicXMLFeed?" + 
                 "command=routeConfig&a=sf-muni&r=N")
responseText = r.text

lastPredict = 9999
arrivals = 0
activePrediction = 0
cycles = 0

while arrivals < trigger:
    q = requests.get(url = "http://webservices.nextbus.com/service/publicXMLFeed?" +
                     "command=predictions&a=sf-muni&stopId=13915&" + 
                     "routeTag=N")
    
    predictions = xp.getPredictions(q.text)
    if lastPredict < predictions[activePrediction]:
        arrivals += 1
    else:
        lastPredict = predictions[activePrediction]
    
    print(predictions[activePrediction])
    
    if predictions[activePrediction] < 120:
        print("ALERT")
        for i in range(5):
            bridge.set_light(6,warnOn)
            time.sleep(1)
            bridge.set_light(6,warnOff)
            time.sleep(1)
        activePrediction += 1
        lastPredict = predictions[activePrediction]
        if cycles != 0:
            print("moving to next train")
            arrivals += 1
        bridge.set_light(6, reset)
    elif 120 <= predictions[activePrediction] <= 300:
        print("updating interim estimate")
        time_left = lastPredict - 120
        thisHue = time_left / 180 * 25500
        lights[6].hue = thisHue
        lights[6].brightness = 255
        lights[6].saturation = 255
    else:
        lights[6].hue = 25500
        lights[6].brightness = 255
        lights[6].saturation = 255
    cycles += 1
    time.sleep(10)


bridge.set_light(6,reset)