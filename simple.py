import sys,requests,os,json,time,math
from elasticsearch import Elasticsearch
import copy 
import nipper_lib
import elastic_creds
import certifi

cla = nipper_lib.parser.parse_args()

if  cla.index_name is None :
	index_name='nipper'
else:
	index_name = cla.index_name

delete_it = cla.delete_index
delete_docs = cla.delete_docs

json_file = "log1_mapped.json"
if cla.file is not None:
	json_file = cla.file

#
#  Read in the JSON from Nipper.  The JSON has already been through map.py to fix some issues
#
NDJSON=1
NORMAL=2
filetype=NDJSON

#JSON can be in an array, or newline delimited. Test to see which
with open(json_file) as fn:
    first = fn.readline()
    if first[0] == '[':
        filetype = NORMAL
    fn.close()
#
#  Read in the JSON from Nipper.  The JSON has already been through map.py to fix some issues
#
print("open {} ".format(json_file))
js=[]
with open(json_file) as fn:
    if filetype == NORMAL:
        js=json.load(fn)
    else:
        for line in fn:
            json_object = json.loads(line)
            js = js + [json_object]
print("read in {} json file ok with {} objects\n".format(filetype,len(js)))

#es = Elasticsearch(elastic_creds.host,httpauth=(elastic_creds.user,elastic_creds.password),port=elastic_creds.port)
es = Elasticsearch(elastic_creds.host, use_ssl=True,verify_certs=False,ca_certs=certifi.where())

print(es.info())


if not es.ping():
	raise ValueError("Can't connect to Elastic")

nipper_lib.initialise_index(es,index_name,delete_it,delete_docs)

i=0
# FOr every document produced by Nipper

# apply some fixes

def dump_error_file(report,filename):
		if  os.path.exists(filename):
			print('file {} already exists - do not overwrite'.format(filename))
		else:
			with open(filename,"w") as ef:
					ef.write("[\n")
					json.dump(report, ef,indent=4)
					ef.write("]\n")

for report in js:
#	if 'audit_type' in report: 
		#Insert it into Elastic
		response = es.index(index=index_name,ignore=400,body=report)
		if 'error' in response:
				print("failure to insert {} ".format(report["nipper_id"]))
				print("---------------------------------------------")
				#print(json.dumps(response,indent=4))
				reason = response['error']['root_cause'][0]['reason']
				print(reason)
				print(response)
		else:
				print(response)
		i = i + 1

