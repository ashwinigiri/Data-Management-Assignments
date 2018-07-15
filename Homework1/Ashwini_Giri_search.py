#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 14:59:26 2018

@author: ashwinigiri
"""


import sys
import requests
import json
import re

inputval = sys.argv[1]
input_lst = []
input_lst = inputval.split(" ")
output_lst=[]

for i in input_lst:
    
    if re.match('^[a-zA-Z]*$',i):
        val = i.upper()
        url = 'https://inf551-8d68c.firebaseio.com/index.json?orderBy="$key"&equalTo="' + val + '"'
        response = requests.get(url)
        data = json.loads(response.content)
    else:
        continue
    #val = i.upper()
    
    if len(data) == 0:
        continue
    else:
        output_lst.extend(data[val])
        
if len(output_lst) == 0:
    print("Oops!! The serch does not match please try with another keyword!!")
else:
    print(output_lst)
