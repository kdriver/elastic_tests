docker system prune -f
docker run -d --name myelastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.5.1
docker run -d --link myelastic:elasticsearch  -p 5601:5601 docker.elastic.co/kibana/kibana:7.5.1
