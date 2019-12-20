import elasticsearch
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file")
parser.add_argument("-n","--index_name")
parser.add_argument("-i","--index_delete",action="store_true")
parser.add_argument("-d","--docs_delete",action="store_true")
parser.add_argument("-r","--repeat",type=int,default=0)

query= { 
    "query" : { 
        "match_all" : {} 
    }
}
settings_old= {
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
settings = {
    "settings": {
        "index": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "mapping.depth.limit": 500,
		    "index.mapping.total_fields.limit" : 50000,
		    "index.mapping.nested_fields.limit" : 50000
        }
    },
    "mappings": {
        "properties": {
            "date_time": {
                "type": "date",
                "format": "EEE MMM d[d] HH:mm:ss yyyy"
            },
            "summary": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 8192
                    }
                }
            },
            "check": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 8192
                    }
                }
            },
            "fix": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 8192
                    }
                }
            },
            "description": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 8192
                    }
                }
            },
            "impact": {
                "properties": {
                    "description": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 8192
                            }
                        }
                    }
                }
            },
            "reccomendation": {
                "properties": {
                    "description": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 8192
                            }
                        }
                    }
                }
            },
            "ease": {
                "properties": {
                    "description": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 8192
                            }
                        }
                    }
                }
            }
        }
    }
}

def delete_contents(es,index_name,delete_it):
    if es.indices.exists(index=index_name):
            print("Index {} exists".format(index_name))
            if delete_it == True:
                print("Delete the index")
                response = es.indices.delete(index=index_name,ignore=[400,404])
                print(response)
                print("deleted Index");
                response = es.indices.create(index=index_name,ignore=400, body=settings)
                print(response)
                print("created index")
            else:
                print("Delete the documents in the index")
                docs = es.search(index=index_name,filter_path=['hits.hits._id'],size=10000,body=query)
                answer = es.delete_by_query(index=index_name,body=query)
                print("deleted {} docs in one go {}".format(len(docs),answer))
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
        
