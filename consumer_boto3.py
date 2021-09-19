from logging import exception
from kafka import KafkaConsumer, TopicPartition
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

"""
bulid broker for just boto3 on exp localhost:8092

"""
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

    boto3
    client = boto3.client(
        's3',
        aws_access_key_id='AKIASRPO5Q5UW6ZZZNUO',
        aws_secret_access_key='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'
        # , region_name='ap-south-1'
    )

    # Creating the high level object oriented interface
    resource = boto3.resource(
        's3',
        aws_access_key_id='',
        aws_secret_access_key=''
        # , region_name='ap-south-1'
    )

    # Boto3 Bucket folder1/Test_File.txt
    obj = client.get_object(
        Bucket='testbucket-nasir',
        Key='folder1/Test_File.txt'
    )

    s3 = resource
    s3object = s3.Object('testbucket-nasir', 'folder1/Test_File.txt')

    print("starting the consumer")
    for msg in consumer:
        print(msg)
        print("Registered User = {}".format(msg.value))
        try:
            json_object = json.dumps(msg.value)
            client.put_object(
                Body=json_object,
                Bucket='testbucket-nasir',
                Key='folder1/Test'
            )
            s3object.put(
                Body=(bytes(json.dumps(msg.value).encode('UTF-8')))
            )
        except Exception as e:
            print("EXeptions are ", e)
        print('push')
