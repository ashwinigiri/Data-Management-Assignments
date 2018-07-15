#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 02:34:15 2018

@author: ashwinigiri
"""
import csv
import sys
import codecs

input_file = str(sys.argv[1])
output_file = str(sys.argv[2])

rd = codecs.open(input_file,'r','utf-8')
fd = codecs.open(output_file,'w','utf-8')
fd.write('<parks>\n')

line = csv.reader(rd,delimiter='\t')

column_names=[]
for row in line:
    column_names = row
    break

def checkRow(string):
    if '&' in string:
        string = string.replace('&','&amp;')
    if '<' in string:
        string = string.replace('<','&lt;')
    if '>' in string:
        string = string.replace('>','&gt;')
    if '\"' in string:
        string = string.replace('\"','&quot;')
    if '\'' in string:
        string = string.replace('\'','&apos;')
    return(string)

for li in line:
    fd.write('\t<park>\n')
    # print('\t<park>')
    for j in range(0,len(column_names)):
        opentag = '\t\t<'+column_names[j]+'>'
        closetag = '</'+column_names[j]+'>\n'
        if type(li[j]) is str:
            string = checkRow(li[j])
        else:
            string = li[j]
        row = opentag+string+closetag
        # print(row)
        fd.write(row)
    # print('\n\t</park>\n')
    fd.write('\t</park>\n')

fd.write('</parks>')