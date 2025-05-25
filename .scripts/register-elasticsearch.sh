curl -i -X POST -H "Accept: application/json" -H "Content-Type: application/json" localhost:8083/connectors/ -d '{
  "name": "elasticsearch",
  "config": {
    "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
    "tasks.max": "1",
    "topics": "catalog-db.codeflix.categories",
    "connection.url": "http://elasticsearch:9200",
    "key.ignore": "true"
  }
}'
