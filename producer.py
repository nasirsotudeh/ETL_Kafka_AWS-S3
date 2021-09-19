from kafka import KafkaProducer
import time
import os
import json
import socket
from data import get_registered_user


def json_serializer(data):
    return json.dumps(data).encode('utf-8')


producer = KafkaProducer(
    bootstrap_servers=os.environ.get('KAFKA_HOST', 'localhost:9092 ,localhost:9094'),
    value_serializer=json_serializer)

conf = {'bootstrap.servers': "localhost:29092",
        'client.id': socket.gethostname()}

# producer_conf = Producer(conf)


if __name__ == "__main__":
    while 1 == 1:
        registered_user = get_registered_user()
        print(registered_user)
        producer.send("hot-topic", registered_user)
        time.sleep(1)
