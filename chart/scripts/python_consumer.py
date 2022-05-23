from kafka import KafkaConsumer
from json import loads
import sys


broker_endpoint=str(sys.argv[1])
topic=str(sys.argv[2])
consume_count=int(sys.argv[3])

# This is a consumer test that communicates with a kafka broker exposed via the Metallb loadbalancer.
consumer = KafkaConsumer(
     topic,
     bootstrap_servers=[broker_endpoint],
     auto_offset_reset='earliest',
     value_deserializer=lambda x: loads(x.decode('utf-8')))


for increment,message in enumerate(consumer):
    message = message.value
    print('Consuming: {} from topic {}'.format(message,topic))
    
    if increment >= consume_count:
        print("exiting")
        break
    
