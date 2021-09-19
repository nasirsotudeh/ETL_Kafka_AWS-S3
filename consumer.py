from logging import exception
from kafka import KafkaConsumer , TopicPartition
import json
import boto3
import time


# import os
# os.environ["AWS_DEFAULT_REGION"] = 'us-east-2'
# os.environ["AWS_ACCESS_KEY_ID"] = 'mykey'
# os.environ["AWS_SECRET_ACCESS_KEY"] = 'mysecretkey'

def json_serializer(data):
    return json.dumps(data).encode("utf-8")


def forgiving_json_deserializer(v):
    try:
        return json.loads(v.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        exception('Unable to decode: %s', v)
        return None

if __name__ == "__main__":
    consumer = KafkaConsumer(
        "registered_user",
        bootstrap_servers='localhost:8092',
        auto_offset_reset='latest',
        # group_id="consumer-group-a",
        value_deserializer=forgiving_json_deserializer
        # auto_offset_reset='earliest'
        # ignore value_deserializer=forgiving_json_deserializer
        # msg = json.loads(msg)
    )
    # list all topics
    # consumer.subscribe([])
    # consumer.assign([TopicPartition('registered_user', 3)])
    time.sleep(1)
    print('Topics : {} '.format(consumer.topics()))
    partitions = consumer.partitions_for_topic('newreplica')

    print("starting the consumer")
    for msg in consumer:
        print(msg)
        print("Registered User = {}".format(msg.value))
        try:
            consumer.subscribe()
        except Exception as e:
            print("EXeptions are ", e)
        print('push')
