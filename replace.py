import sys,requests,os,json,time,math
from elasticsearch import Elasticsearch

directory='.'
index_name='nipper'


if len(sys.argv) > 1 :
	json_file = sys.argv[1]
else:
	json_file = "mapped.json"

i=1
#
#  Read in the JSON from Nipper.  The JSON has already been through map.py to fix some issues
#
print("open {} ".format(json_file))
with open(json_file) as fn:
	js=json.load(fn)

#
#  Open elasticsearcj
#
res = requests.get('http://localhost:9200')
#print(res.content,end='\n')
es = Elasticsearch([{'host':'localhost','port':'9200'}])
#es = Elasticsearch(['http://elastic:changeme@192.168.0.113:9200'])
#print(response)

#
#  Delete all the documents in the index.  
#  This is better than deleting the index, which breaks Kabana's visualisation
#
query= { 
    "query" : { 
        "match_all" : {} 
    },
    "stored_fields": []
}
settings= {
        "settings": {
                "number_of_shards" : 1,
                "number_of_replicas" : 0,
		"index.mapping.depth.limit" : 50,
		"index.mapping.total_fields.limit": 5000
        },
	"mappings": {
		"properties": {
			"date_time" : { "type" : "date", "format" :    "EEE MMM d[d] HH:mm:ss yyyy" }
		}
	}
}
command="curl -H \"Content-Type: application/json\" -X POST \"http://localhost:9200/" + str(index_name)+ "/_delete_by_query\" -d '{ \"query\": { \"match_all\" : {} } }'"

#delete it, or delete the documents within
response = es.indices.delete(index=index_name,ignore=[400,404])

if es.indices.exists(index=index_name):
		os.system(command)
		docs = es.search(index=index_name,filter_path=['hits.hits._id'],size=10000,body=query)
		if len(docs) > 0 :
			ids = [d['_id'] for d in docs['hits']['hits']]
			total = len(ids)
			print("deleting {} docs".format(total))
			i=0
			for id in ids:
				es.delete(index=index_name,id=id)
				print("deleting {} % complete".format(math.floor(i/total*100)),end='\r')
				i=i+1
		print("deleted")
else:
		response = es.indices.create(index=index_name,ignore=400, body=settings)
		print(response)


#
#   fix JSON entries that have an empty body - invalid JSON?
#
def fix(report,name):
	if report[name] == ['']:
		print("match {}  --> ".format(name),end="")
		report[name] = []
		response = es.index(index=index_name,ignore=400,id=i,body=report)
		if 'error' in response:
				print(response)
				exit()
		else:
				print("fixed nipper_id {}".format(report['nipper_id']))

i=0
# FOr every document produced by Nipper
for report in js:
	if 'audit_type' in report: 
		#Insert it into Elastic
		response = es.index(index=index_name,ignore=400,id=i,body=report)
		i = i + 1
		print(".",end='',flush=True)
		if 'error' in response:
			print("\n")
			# If elastic returns an error, try to fix the problem and re-insert
			print("--found an error in {}".format(report['nipper_id']))
			if 'advisories' in report:
				fix(report,'advisories')
				fix(report,'references')
			else:
				# The only way I've found to fix the findings entries is to delete them
				print(str(response))
				if "finding " in str(report) :
					print("findings {}".format(report['findings']))
					x = report['findings']
					y = list(x.keys())[0] 
					print(y)
					co = report['findings'][y]
					del report['findings'][y]
					report['findings']["device"] = co
					print(report['findings'])
				# Try one last time after applying the fix
				response = es.index(index=index_name,ignore=400,id=i,body=report)
				if 'error' in response:
						# game over - error is still there
						print("THE FIX FAILED")
						print(json.dumps(report,indent=4))
						with open('error.json', 'w') as outfile:
							outfile.write("[\n")
							json.dump(report, outfile,indent=4)
							outfile.write("]\n")
						print(json.dumps(response,indent=4))
						print("Delete findings - desperate measure")
						co = report['findings']
						del report['findings']
						response = es.index(index=index_name,ignore=400,id=i,body=report)
						if 'error' in response:
							print("give up")
							exit()
						else:
							print("Fixed with a sledgehammer")
				else:
						print("{}".format(report['findings']))
						print("findings fixed nipper_id {} ".format(report['nipper_id']))
				
					
