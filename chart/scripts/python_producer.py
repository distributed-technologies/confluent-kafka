from time import sleep
from json import dumps
from kafka import KafkaProducer
import sys


broker_endpoint=str(sys.argv[1])
topic=str(sys.argv[2])

# This is a producer test that communicates with a kafka broker exposed via the Metallb loadbalancer.
producer = KafkaProducer(bootstrap_servers=[broker_endpoint],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

print("Connected")
for number in range(11):
    data = {'number' : number, 'category': 'test' }
    print('Producing: {} on topic {} \n'.format(data['number'],topic))
    producer.send(topic, value=data)
    sleep(1)
