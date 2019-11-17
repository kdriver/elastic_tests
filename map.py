import requests,os,json,time

directory='.'
i=1

for filename in os.listdir(directory):
	if filename.endswith('all.json'):
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
	if  'findings' in report:
		x = report['findings']
		y = list(x.keys())
		for k in y:
			z = report['findings'][k]
			if '-' in k:
				#print("replacing {} ".format(k),end='')
				kk = k.replace('-','_')
				#print(kk)
				del report['findings'][k]
				report['findings'][kk] =z
			if "CiscoIOS15" == k:
				del report['findings'][k]
				report['findings']["CiscoIOStree"] = z
		for k in report['findings'] :
			f = report['findings'][k]
			for g in f:
				finding = report['findings'][k][g]
				if isinstance(finding,dict):
					#print(finding)
					for item in finding:
						if item == '':
							#print("found null")
							co = finding[item]
							report['findings'][k][g]["kdd"] = co
							del report['findings'][k][g][item]
				#print(report['findings'][k][g])
							
with open("mapped.json","w") as wf:
	json.dump(js, wf, indent=4)
	
