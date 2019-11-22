import sys,requests,os,json,time,math
from elasticsearch import Elasticsearch

directory='.'
index_name='test-syntax'
delete_it = False


if len(sys.argv) > 1 :
	json_file = sys.argv[1]
	if len(sys.argv) > 2:
		if sys.argv[2] == "True":
			delete_it = True
			print("delete the index - not just the docs in it")
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
if delete_it== True:
	response = es.indices.delete(index=index_name,ignore=[400,404])
	print(response)
	print("deleted Index");

#
#  Delete all the documents in the index.  
#  This is better than deleting the index, which breaks Kabana's visualisation
#
query= { 
    "query" : { 
        "match_all" : {} 
    }
}
settings= {
        "settings": {
                "number_of_shards" : 1,
                "number_of_replicas" : 0,
		"index.mapping.depth.limit" : 500,
		"index.mapping.total_fields.limit" : 50000,
		"index.mapping.nested_fields.limit" : 50000
        },
	"mappings": {
		"properties": {
			"date_time" : { "type" : "date", "format" :    "EEE MMM d[d] HH:mm:ss yyyy" }
		}
}
}

if es.indices.exists(index=index_name):
		docs = es.search(index=index_name,filter_path=['hits.hits._id'],size=10000,body=query)
		answer = es.delete_by_query(index=index_name,body=query)
		print("deleted {} docs ins one go {}".format(len(docs),answer))
		#docs = es.search(index=index_name,filter_path=['hits.hits._id'],size=10000,body=query)
		#if len(docs) > 0 :
	#		ids = [d['_id'] for d in docs['hits']['hits']]
	#		total = len(ids)
	#		print("deleting {} docs".format(total))
	#		i=0
	#		for id in ids:
	#			es.delete(index=index_name,id=id)
	#			print("deleting {} % complete".format(math.floor(i/total*100)),end='\r')
	#			i=i+1
	#	print("deleted")
else:
		response = es.indices.create(index=index_name,ignore=400, body=settings)
		print(response)
		print("created index")
	
time.sleep(5)


# FOr every document produced by Nipper
for report in js:
	if 'audit_type' in report: 
		#Insert it into Elastic
		response = es.index(index=index_name,ignore=400,id=i,body=report)
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
				
					
