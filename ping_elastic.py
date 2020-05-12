from elasticsearch import Elasticsearch
import elastic_creds
import nipper_lib
import certifi
import urllib3

urllib3.disable_warnings()

cla = nipper_lib.parser.parse_args()

if  cla.index_name is None :
	index_name='nipper'
else:
	index_name = cla.index_name

#es = Elasticsearch(elastic_creds.host,httpauth=(elastic_creds.user,elastic_creds.password),port=elastic_creds.port,use_ssl=False)
es = Elasticsearch(elastic_creds.host, use_ssl=True,verify_certs=False,ca_certs=certifi.where())

print(es)
print(es.info())


#if not es.ping():
#    raise ValueError("Can't connect to Elastic")