import requests,os,json,time,uuid

directory='.'
i=1

for filename in os.listdir(directory):
	if filename.endswith('log1.json'):
		with open(filename) as fn:
			js=json.load(fn)
i=1000
for report in js:
	report['nipper_id'] = i
	i = i + 1
	if  'advisories' in report:
		if report['advisories'] == ['']:
			report['advisories'] = []
	if  'references' in report:
		if report['references'] == ['']:
			report['references'] = []
	if 'finding' in report:
		f = report['finding']
		if 'table' in f:
			del report['finding']['table']
			report['finding']['table'] = "replaced recursive table"
	if 'summary' in report:
		co = report['summary'][0]
		report['summary'] = co

	if  'findings' in report:
		#x = report['findings']
		#y = list(x.keys())
		#for k in y:
		#	z = report['findings'][k]
		#	if '-' in k:
		#		#print("replacing {} ".format(k),end='')
		#		kk = k.replace('-','_')
		#		#print(kk)
		#		del report['findings'][k]
		#		report['findings'][kk] =z
		#	if "CiscoIOS15" == k:
		#		del report['findings'][k]
		#		report['findings']["CiscoIOStree"] = z
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
							
def report_it(report,skip):
	answer = True
	if  'finding_id' in report:
		if report['finding_id'] == skip:
			answer = False
	return answer

def dump_files(skip):
	with open("log1_mapped.json","a") as wf:
		for report in js:
			if report_it(report,skip) :
				the_s = json.dumps(report)
				wf.write(the_s + '\n')
		wf.close()
	with open("10.json","a") as wf:
		for index in range(0 , 10):
			if report_it(report,skip) :
				the_s = json.dumps(js[index])
				wf.write(the_s + '\n')
		wf.close()
	with open("1000.json","a") as wf:
		for index in range(0 , 1000):
			if report_it(report,skip) :
				the_s = json.dumps(js[index])
				wf.write(the_s + '\n')
		wf.close()
	with open("2000.json","a") as wf:
		for index in range(0 , 2000):
			if report_it(report,skip) :
				the_s = json.dumps(js[index])
				wf.write(the_s + '\n')
		wf.close()
	with open("log1_formatted.json","a") as wf:
		json.dump(js, wf, indent=4)
	
def delete_it(filename):
	if os.path.exists(filename):	
		os.remove(filename)

delete_it("log1_mapped.json")
delete_it("10.json")
delete_it("100.json")
delete_it("1000.json")
delete_it("2000.json")
delete_it("log1_formatted.json")

session_uuid = str(uuid.uuid4())
print(session_uuid)
for report in js:
	report['nipper_session'] = session_uuid
	report['nipper_text'] = "Research Network first audit" 
dump_files("")
session_uuid = str(uuid.uuid4())
print(session_uuid)
for report in js:
	report['nipper_text'] = "Research Network second audit" 
	report['nipper_session'] = session_uuid
dump_files("V-3062")

