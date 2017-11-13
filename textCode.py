#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 19:03:38 2017

@author: frouglas
"""

import xmlParser as xp
import requests
import xml.etree.ElementTree as ET

q = requests.get(url = "http://webservices.nextbus.com/service/publicXMLFeed?" +
                 "command=predictions&a=sf-muni&stopId=13915&" + 
                 "routeTag=N")

root = ET.fromstring(q.text)

breakPt = 1