from kafka import KafkaAdminClient
from kafka import KafkaConsumer
from kafka.structs import TopicPartition
from kafka.admin import NewPartitions

'''
this script add 1 partition each time run

'''


BROKER_URL = "192.168.122.1:9092"
if __name__ == "__main__":
    cluser = KafkaAdminClient(bootstrap_servers='192.168.122.1:9092')

    # cluser.create_partitions(topic_partitions='registered_user',
    #                          timeout_ms=100,
    #                          validate_only=False,
    #                          )

    topic = 'registered_user'
    bootstrap_servers = '192.168.122.1:9092'
    consumer = KafkaConsumer(
        topic, bootstrap_servers=bootstrap_servers, auto_offset_reset='earliest')

    partitions = consumer.partitions_for_topic(topic)
    for i in partitions:
        i = i + 1

    topic_partitions = {}
    topic_partitions[topic] = NewPartitions(total_count= i + 1)
    cluser.create_partitions(topic_partitions)
    partitions1 = consumer.partitions_for_topic(topic)
    print(partitions1)