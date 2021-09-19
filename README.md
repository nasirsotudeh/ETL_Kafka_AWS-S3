# Streaming data from Kafka to S3 using Kafka Connect

```
~/Docker:docker-compose up -d
```

```
    Name                  Command               State                    Ports
---------------------------------------------------------------------------------------------
broker            /etc/confluent/docker/run   Up             0.0.0.0:9092->9092/tcp
kafka-connect     bash -c #                   Up (healthy)   0.0.0.0:8083->8083/tcp, 9092/tcp
                  echo "Installing ...
ksqldb            /usr/bin/docker/run         Up             0.0.0.0:8088->8088/tcp
schema-registry   /etc/confluent/docker/run   Up             0.0.0.0:8081->8081/tcp
zookeeper         /etc/confluent/docker/run   Up             2181/tcp, 2888/tcp, 3888/tcp

```

Create the Sink connector from config file
we can run multi connector


```
curl -i -X PUT -H "Accept:application/json" \
    -H  "Content-Type:application/json" http://localhost:8083/connectors/sink-s3-voluble/config \
    -d '
 {
		"connector.class": "io.confluent.connect.s3.S3SinkConnector",
		"key.converter":"org.apache.kafka.connect.storage.StringConverter",
		"tasks.max": "1",
		"topics": "cats",
		"s3.region": "us-east-1",
		"s3.bucket.name": "rmoff-voluble-test",
		"flush.size": "65536",
		"storage.class": "io.confluent.connect.s3.storage.S3Storage",
		"format.class": "io.confluent.connect.s3.format.avro.AvroFormat",
		"schema.generator.class": "io.confluent.connect.storage.hive.schema.DefaultSchemaGenerator",
		"schema.compatibility": "NONE",
        "partitioner.class": "io.confluent.connect.storage.partitioner.DefaultPartitioner",
        "transforms": "AddMetadata",
        "transforms.AddMetadata.type": "org.apache.kafka.connect.transforms.InsertField$Value",
        "transforms.AddMetadata.offset.field": "_offset",
        "transforms.AddMetadata.partition.field": "_partition"
	}
'

```
Or

curl -i -X PUT -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/sink-s3-voluble3/config -d @config.json


_________________________________________________________________________________

If you want to create the data generator and list data in ksqlDB:


```docker exec -it ksqldb ksql http://ksqldb:8088```


and push all form [Fake-datastream-ksql](kafka-connect/confluent/Fake-datastream-ksql) in ksql

```
SHOW TOPICS ;

SHOW CONNECTORS;

```
### check config

```
curl -sX GET http://localhost:8083/connectors/sink-s3-voluble3/config | jq
```

### status 
```
curl -s "http://localhost:8083/connectors/sink-s3-voluble/status"| \
    jq -c -M '[.name,.tasks[].state]'
```
### DELETE CONNECTORS :
```
curl -X DELETE http://localhost:8083/connectors/<connector-name>
```

### pause
```
curl -X PUT localhost:8083/connectors/connectorName/pause
```
______
status 

# get staus all connectors

curl -s "http://localhost:8083/connectors"|   jq '.[]'|   xargs -I{connector_name} curl -s "http://localhost:8083/connectors/"{connector_name}"/status"|   jq -c -M '[.name,.connector.state,.tasks[].state]|join(":|:")'|   column -s : -t| sed 's/\"//g'| sort




# get status each connector with name
curl -s -X GET http://localhost:8083/connectors/{connector_name}/status
ex :
curl -s -X GET http://localhost:8083/connectors/s3_sink_lson/status



# get tasks each connector with name

curl -s -X GET http://localhost:8083/connectors/s3_sink_druid/tasks |jq



_____________________________________


## for add more broker we can use :
```
  docker run -it --rm --net=confluent_default--name=kafka-1 -e KAFKA_BROKER_ID=2 -p 8092:8092 -e depends_on=zookeeper -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka-1:39093,PLAINTEXT_HOST://localhost:8092 \
  -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181  confluentinc/cp-kafka:5.4.1
  ```
  ## for add more broker we can use :
```

docker run -it --rm --net=confluent_default --name=kafka-2 \ 
-e KAFKA_BROKER_ID=3 -p 7092:7092 \
-e depends_on=zookeeper \
-e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT \
-e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka-2:49094,PLAINTEXT_HOST://localhost:7092 \
-e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181  confluentinc/cp-kafka:5.4.1



```
delete all containers

```
docker rm -f $(docker ps -a | grep -v CONTAINER | awk '{print $1}')
```


## in other ways we can use 
 docker run -d \
  --name=connect-stage \
  --net=host \
  -e CONNECT_BOOTSTRAP_SERVERS="localhost:92092" \
  -e CONNECT_REST_PORT=8081 \
  -e CONNECT_GROUP_ID="test-connect-cluster" \
  -e CONNECT_CONFIG_STORAGE_TOPIC="connect-configs" \
  -e CONNECT_OFFSET_STORAGE_TOPIC="connect-offsets" \
  -e CONNECT_STATUS_STORAGE_TOPIC="connect-statuses" \
  -e CONNECT_KEY_CONVERTER="io.confluent.connect.avro.AvroConverter" \
  -e CONNECT_VALUE_CONVERTER="io.confluent.connect.avro.AvroConverter" \
  -e CONNECT_KEY_CONVERTER_SCHEMA_REGISTRY_URL="http://xxx:8081" \
  -e CONNECT_VALUE_CONVERTER_SCHEMA_REGISTRY_URL="http://xxx:8081" \
  -e CONNECT_INTERNAL_KEY_CONVERTER="org.apache.kafka.connect.json.JsonConverter" \
  -e CONNECT_INTERNAL_VALUE_CONVERTER="org.apache.kafka.connect.json.JsonConverter" \
  -e CONNECT_REST_ADVERTISED_HOST_NAME="localhost" \
  -e AWS_ACCESS_KEY_ID="..." \
  -e AWS_SECRET_ACCESS_KEY="..." \
  confluentinc/cp-kafka-connect:latest

```
