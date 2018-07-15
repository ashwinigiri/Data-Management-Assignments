import csv
from lxml import etree
import sys
import codecs

location_type_dict = {}
input_file = str(sys.argv[1])
f = codecs.open(input_file,'r','utf-8')

tree = etree.parse(f)
for element in tree.xpath("//LocationType"):
    location_type_dict[element.text] = 0

for key,value in location_type_dict.items():
    for element in tree.xpath("//LocationType"):
        if key == element.text:
            value += 1
            location_type_dict[key] = value

for key in sorted(location_type_dict):
    print("%s   %s" %(key, location_type_dict[key]))
