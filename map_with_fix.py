import requests,os,json,time,uuid
import argparse
from datetime import datetime
from datetime import timedelta

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file",default="log1.json")
parser.add_argument("-t","--twice",action='store_true',default=False)
parser.add_argument("-r","--repeat",type=int,default=0)
cla = parser.parse_args()
print(cla)
import copy

def delete_it(filename):
	if os.path.exists(filename):	
		os.remove(filename)

json_file = "nipper.json"
if cla.file is not None:
    json_file = cla.file

directory='.'

#open the source logfile from nipper - coded so a list of jason files can be processed, but we only take in 1
delete_it("fix_list.json")
fixes = open("fix_list.json","w")

i=0

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

#for each JSON record

#replace attributes tha have an empty array specified [""]
#replace a very deep recursive table structure
#within a recird search findings where we have empty attribute names items in a dictionary

delete_it("log1_original_nd.json")
org = open("log1_original_nd.json","w") 
i=0
t1= datetime.now()
for report in js:
	unmodified = copy.deepcopy(report)
	report['nipper_id'] = i
	the_s = json.dumps(report)
	org.write(the_s + '\n')

	i = i + 1
	fix_list=[]
	report['date_time'] = t1.strftime("%a %b %d %H:%M:%S %Y")

	if  'never_advisories' in report:
		if report['advisories'] == ['']:
			report['advisories'] = []
			fix_list = fix_list + ["advisories"]
	if  'never_references' in report:
		if report['references'] == ['']:
			report['references'] = []
			fix_list = fix_list + ["references"]
	if 'never_finding' in report:
		f = report['finding']
		if 'table' in f:
			del report['finding']['table']
			report['finding']['table'] = "replaced recursive table"
			fix_list = fix_list + ["replaced recursive table"]
	if 'never_summary' in report:
		co = report['summary'][0]
		report['summary'] = co
		fix_list = fix_list + ["summary"]

	if  'never_findings' in report:
		for k in report['findings'] :
			f = report['findings'][k]
			for g in f:
				finding = report['findings'][k][g]
				if isinstance(finding,dict):
					for item in finding:
						if item == '':
							co = finding[item]
							report['findings'][k][g]["kdd"] = co
							del report['findings'][k][g][item]
							fix_list = fix_list + ["replaced null finding name"]
	if len(fix_list) > 0:
		print("{} fixed {} ".format(i-1,fix_list))
		report['nipper_fix_list'] = fix_list
		debugit = [ unmodified, report ]
		fixes.write(json.dumps(debugit,indent=4))
	
fixes.close()
org.close()
							
#a small function to facilitate skipping a defined finding id so that we get different results in separate runs
def report_it(report,skip):
	answer = True
	if  'finding_id' in report:
		if report['finding_id'] == skip:
			answer = False
	return answer

# a function to dump out the output in different formats ( formatted and ndjson ) and to have some with 10,1000,2000 records in them  for debuggig
# all files are appended to, hence the need to delete this scriots previous runs files explicity
def dump_files(skip):
	with open("log1_mapped.json","a") as wf:
		for report in js:
			if report_it(report,skip) :
				the_s = json.dumps(report)
				wf.write(the_s + '\n')
		wf.close()
	with open("10.json","a") as wf:
		for index in range(0 , 10):
			report = js[index]
			if report_it(report,skip) :
				the_s = json.dumps(report)
				wf.write(the_s + '\n')
		wf.close()

	with open("log1_formatted.json","a") as wf:
		json.dump(js, wf, indent=4)
	
	if len(js) < 1000:
		return
	
	with open("1000.json","a") as wf:
		for index in range(0 , 1000):
			report = js[index]
			if report_it(report,skip) :
				the_s = json.dumps(report)
				wf.write(the_s + '\n')
		wf.close()

	if len(js) < 2000:
		return
	with open("2000.json","a") as wf:
		for index in range(0 , 2000):
			report = js[index]
			if report_it(report,skip) :
				the_s = json.dumps(report)
				wf.write(the_s + '\n')
		wf.close()
	
#delete a filename - checking that it exists first 
def delete_it(filename):
	if os.path.exists(filename):	
		os.remove(filename)

#delete all files this script generates before we regenerate them
delete_it("log1_mapped.json")
delete_it("10.json")
delete_it("100.json")
delete_it("1000.json")
delete_it("2000.json")
delete_it("log1_formatted.json")

#a UUID to uniquly identify this run
session_uuid = str(uuid.uuid4())
print(session_uuid)
#for every report in the original add the UUID and some text
for report in js:
	report['nipper_session'] = session_uuid
	report['nipper_text'] = "Research Network first audit" 
	report['date_time'] = t1.strftime("%a %b %d %H:%M:%S %Y")

#dump the output, but dont skip any finding
dump_files("")

skip_finding="V-3062"
#if cla.twice == True:
if cla.repeat != 0:
	for day in range(1,cla.repeat):
		t1 = datetime.now() - timedelta(days=day)
		t1_str = t1.strftime("%a %b %d %H:%M:%S %Y")
		print('Dump again with missing finding ID {} time {} '.format(skip_finding,t1_str))
		session_uuid = str(uuid.uuid4())
		print(session_uuid)
		#for every report in the original add  a different UUID and text. This simulates a second audit
		for report in js:
			report['nipper_text'] = "Research Network audit" 
			report['nipper_session'] = session_uuid
			report['date_time'] = t1_str
		#dump the files , skipping a finding ID
		dump_files(skip_finding)

#  time.strftime("%a %b %d %H:%M:%S %Y")
