import sys,requests,os,json,time,math
from elasticsearch import Elasticsearch
import copy 
import nipper_lib
import elastic_creds

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

es = Elasticsearch(elastic_creds.host,httpauth=(elastic_creds.user,elastic_creds.password),port=elastic_creds.port)
print(es.info())


if not es.ping():
	raise ValueError("Can't connect to Elastic")

nipper_lib.initialise_index(es,index_name,delete_it,delete_docs)

time.sleep(1)
i=0
# FOr every document produced by Nipper

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

# apply some fixes
def kdd_fixit(report,response):
	if cla.dont_fix:
		return False
	answer = True
	if 'findings' in reason:
		fix = report['findings']	
		#print(json.dumps(fix,indent=4))
		#replace the 'findings' entry with one named 'finding_list'
		report['finding_list'] = fix
		item = list(fix.keys())[0]
		#findings=list(fix[item].keys())
		#for f in findings:
		#	content = fix[item][f]
		#	fix[item]['finding'] = content
		#	del fix[item][f]
		#and delete the child item ( usually the hostname string) content and replace it with text to say we've changed it.
		del fix[item]
		fix[item] = 'replaced by fixit'
		del report['findings']
	
	response = es.index(index=index_name,ignore=400,body=report)
	if 'error' in response:
		answer = False
		print('Failed to fix it ')
	else:
		print(response)
	return answer

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
				a_copy = copy.deepcopy(report)
				print("failure to insert {} ".format(report["nipper_id"]))
				print("---------------------------------------------")
				#print(json.dumps(response,indent=4))
				reason = response['error']['root_cause'][0]['reason']
				print(reason)
				print(response)
				if kdd_fixit(report,reason) == False:
					print(json.dumps(report,indent=4))
					error_filename = str("errors/") + str(report["nipper_id"]) + ".json"
					dump_error_file(report,error_filename)
					print("give up : offending document written to {}.json".format(report["nipper_id"]))
					print("---------------------------------------------")
					exit()
				else:
					a_copy['error_report'] = reason
					error_filename = str("errors/") + str("fixed_") + str(report["nipper_id"]) + ".json"
					dump_error_file(a_copy,error_filename)
					print('Fixed it')
		else:
				print(response)
		i = i + 1

