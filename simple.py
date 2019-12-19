import sys,requests,os,json,time,math
from elasticsearch import Elasticsearch
import nipper_lib

cla = nipper_lib.parser.parse_args()

if  cla.index_name is None :
	index_name='test-syntax'
else:
	index_name = cla.index_name

delete_it = cla.index_delete
delete_docs = cla.docs_delete

json_file = "mapped.json"
if cla.file is not None:
	json_file = cla.file

#
#  Read in the JSON from Nipper.  The JSON has already been through map.py to fix some issues
#
print("open {} ".format(json_file))
with open(json_file) as fn:
	js=json.load(fn)

#es = Elasticsearch([{'host':'localhost','port':'9200'}])
es = Elasticsearch(["https://https://a3564804ce99495a9b10ade54bf11653.us-east-1.aws.found.io"],httpauth=('keith','simple'),port=9243)
print(es.info())
#es = Elasticsearch(['http://elastic:changeme@192.168.0.113:9200'])

if not es.ping():
	raise ValueError("Can't connect to Elastic")

# delete the documents in the index, optionally be deleting the index
if delete_docs or delete_it:
	nipper_lib.delete_contents(es,index_name,delete_it)

time.sleep(1)
i=0
# FOr every document produced by Nipper
#js.reverse()
if cla.repeat:
	print("repeat insert the same doc {} times".format(cla.repeat))
	report=js[0]
	while i < cla.repeat:
		response = es.index(index=index_name,ignore=400,body=report)
		if 'error' in response:
			print("\nfailure to insert")
			print("---------------------------------------------")
			print(json.dumps(report,indent=4))
			print(json.dumps(response,indent=4))
			exit()
		else:
				i = i + 1
				print(".",end='',flush=True)
				if (i % 100) == 0:
					print(i,end='')
	print("\n")
	res= es.count(index=index_name,body={'query':{'match_all':{}}})
	print("There are now {} docs in the index".format(res['count']))
	exit()

for report in js:
	if 'audit_type' in report: 
		#Insert it into Elastic
		response = es.index(index=index_name,ignore=400,body=report)
		i = i + 1
		if 'error' in response:
				print("failure to insert")
				print("---------------------------------------------")
				print(json.dumps(report,indent=4))
				print(json.dumps(response,indent=4))
				with open(str(report["nipper_id"]) + ".json","w") as ef:
					ef.write("[\n")
					json.dump(report, ef,indent=4)
					ef.write("]\n")
				print("give up : offending document written to {}.json".format(report["nipper_id"]))
				print("---------------------------------------------")
				exit()
		else:
				print(response)


