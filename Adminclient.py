from confluent_kafka.admin import AdminClient, NewTopic
import click

BROKER_URL = "localhost:9092 , localhost:8092"


def topic_exists(client, topic_name):
    """Checks if the given topic exists"""
    topic_metadata = client.list_topics(timeout=5)
    for t in topic_metadata.topics.values():
        if t.topic == topic_name:
            return True
    return False


def list_all_topics(client):
    """Lists all the available topics"""
    topic_metadata = client.list_topics(timeout=5)
    for t in topic_metadata.topics.values():
        print(t.topic)


def create_topic(client, topic_name, partition ,replica):
    """Creates the topic with the given topic name"""
    futures = client.create_topics(
        [
            NewTopic(
                topic=topic_name,
                num_partitions=partition,
                replication_factor=replica,
                config={
                    "cleanup.policy": "delete",
                    "compression.type": "lz4",
                    "delete.retention.ms": "2000",
                    "file.delete.delay.ms": "2000",
                },
            )
        ]
    )

    for topic, future in futures.items():
        try:
            future.result()
            print("topic created")
        except Exception as e:
            print(f"failed to create topic {topic_name}: {e}")


def main(name, partition , replica):
    """Checks for topic and creates the topic if it does not exist"""
    client = AdminClient({"bootstrap.servers": BROKER_URL})
    # list all available topics
    list_all_topics(client)

    # check if a given topic already exists
    topic_name = name
    if topic_exists(client, topic_name):
        print(f"{topic_name} already exists")

    else:
        print(f"{topic_name} doesn't exist")
        create_topic(client, topic_name, partition , replica)


if __name__ == "__main__":
    if click.confirm('create topic : ?', default=True):
        print('set name for Topic')
        name = input()
        print(' set number of partition :')
        partition = int(input())
        print(' set number of replication :')
        replica = int(input())
        main(name, partition ,replica)
