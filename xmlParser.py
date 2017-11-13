#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 18:57:09 2017

@author: frouglas
"""

import xml.etree.ElementTree as ET

def getPredictions(resultText):
    root = ET.fromstring(resultText)
    
    predictions = []
    
    for direction in root[0].findall('direction'):
        for prediction in direction.findall('prediction'):
            predictions.append(prediction.attrib['seconds'])
    predictions = [int(i) for i in predictions]
    predictions.sort()
    return predictions
        