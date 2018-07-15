#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 18:21:13 2018

@author: ashwinigiri
"""



import pandas as pd
import sys
import requests
import json
import re

input_file = sys.argv[1]

csv_file = pd.DataFrame(pd.read_csv(input_file, sep = ",", header = 0, index_col = False))
csv_file.to_json("menu-136.json",orient = "records",date_format = "epoch",double_precision = 10, 
                 force_ascii = True,date_unit = "ms",default_handler = None)

data = json.load(open("menu-136.json"))
response = requests.put('https://inf551-8d68c.firebaseio.com/menu.json', json=data)

index = {}
index_long = {}


# for adding values in index dictionary

for i in range(len(data)):
    key = data[i].get('event')
    value = [data[i].get('id')]
    val_index = index.get(key)
    if val_index is not None:
        val = index.get(key)
        val.extend(value)
    else:
        index[key]=value
del index[None]

for key,values in index.items():
    if re.match('^[a-zA-Z]*$',key):
        continue
    else:
        index_long[key] = values
        

for key,value in index_long.items():
    del index[key]


for key,value in index_long.items():
    #del index[key]
    key = re.split(';| |&|-',key)
    for i in range(len(key)):
        val = index.get(key[i])
        if val is not None:
            index[key[i]] = val + value
        else:
            index[key[i]] = value
del index['']
#print(index)

response = requests.put('https://inf551-8d68c.firebaseio.com/index.json', json=index)
print("\t\t\t******INDEX******")
print(index)
                