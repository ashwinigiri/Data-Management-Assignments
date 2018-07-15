import json
import sys
from operator import add
from pyspark import SparkContext

sc=SparkContext(appName="ashwiniinf551")

input_file=sys.argv[1]
output_file=sys.argv[2]

input_data=sc.textFile(input_file)

def check_age(input_val):
    line=json.loads(input_val)
    if line['age']>=20 and line['age']<=30:
        return True
    else:
        return False

def return_tuple(input_val):
    line=json.loads(input_val)
    return (line['state'],line['balance'])

def calculate_avg(input_val):
    addition=sum(input_val[1])
    count=float(len(input_val[1]))
    average=addition/count
    return (input_val[0],average)

output_data = input_data.filter(check_age).map(return_tuple).groupByKey().map(calculate_avg).collect()

file_pointer = open(output_file,'w')

for line in output_data:
    file_pointer.write(str(line[0])+','+str(line[1])+'\n')

