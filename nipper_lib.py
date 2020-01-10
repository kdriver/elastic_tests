import elasticsearch
import argparse
from index_settings import settings

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file")
parser.add_argument("-n","--index_name")
parser.add_argument("-i","--delete_index",action="store_true")
parser.add_argument("-d","--delete_docs",action="store_true")
parser.add_argument("-x","--dont_fix",action="store_true")
parser.add_argument("-o","--once",action="store_true")
parser.add_argument("-r","--repeat",type=int,default=0)

query= { 
    "query" : { 
        "match_all" : {} 
    }
}

def create_index(es,index_name):
	response = es.indices.create(index=index_name,ignore=400, body=settings)
	print(response)
	print("created index {}".format(index_name))

def initialise_index(es,index_name,delete_it,delete_docs):
    if es.indices.exists(index=index_name):
            print("Index {} exists".format(index_name))
            if delete_it == True:
                print("Delete the index")
                response = es.indices.delete(index=index_name,ignore=[400,404])
                print(response)
                print("deleted Index");
                create_index(es,index_name)
            else:
                print("Delete the documents in the index")
                docs = es.search(index=index_name,filter_path=['hits.hits._id'],size=10000,body=query)
                answer = es.delete_by_query(index=index_name,body=query)
                print("deleted {} docs in one go {}".format(len(docs),answer))
    else:
             create_index(es,index_name)
        
