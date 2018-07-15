import json
import sys
from operator import add
from pyspark import SparkContext

sc=SparkContext(appName="ashwiniinf551")

input_file =sys.argv[1]
output_file =sys.argv[2]

input_data=sc.textFile(input_file)

def remove_digits(address,accnt_no):
    address=''.join(i for i in address if not i.isdigit())
    return address,accnt_no

output_data = input_data.map(json.loads).map(lambda x:(remove_digits(x['address'],x['account_number']))).filter(lambda x:x!=None).flatMap(lambda(address,account):[(word,account) for word in address.lower().split()]).groupByKey().map(lambda x : (x[0], list(x[1]))).collect()

file_pointer = open(output_file,"w")

for tup in output_data:
    file_pointer.write(str(tup[0])+':'+str(tup[1])+'\n')
