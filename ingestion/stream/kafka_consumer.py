from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "inventory_updates",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Kafka consumer started...")

for message in consumer:

    event = message.value

    print("New inventory update received:")
    print(event)

    # future logic:
    # transform record
    # create embedding
    # update vector DB