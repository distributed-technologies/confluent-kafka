from ksql import KSQLAPI
import sys
import string
import random
import json
import time 

print("Connectiong to ksql server")
endpoint=str(sys.argv[1])
timeout=60

client = KSQLAPI(endpoint,timeout=timeout)
print("Connected")
## Create a non-materialized table with new topic
random_topic = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
stream_name_random = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
materialized_table_random_name = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
print(f"topic: {random_topic}, stream: {stream_name_random}, mat: {materialized_table_random_name}")


client.ksql(f"""CREATE STREAM {stream_name_random} (CATEGORY VARCHAR KEY, NUMBER INT) 
                WITH (KAFKA_TOPIC='{random_topic}', 
                        PARTITIONS=1, 
                        REPLICAS=2, 
                        VALUE_FORMAT='JSON')""")


query_res = client.ksql("LIST STREAMS;")
stream_names = [stream['name'] for stream in query_res[0]['streams']]

if stream_name_random in stream_names:
    print("Stream created")
else:
    print("Stream not created")
    exit(1)

result = client.inserts_stream(stream_name_random, [{ "category": "test", "number": 5 },{ "category": "test", "number": 6 }])
print(result)

# Create a materialized table from table for everything
client.ksql(f"CREATE TABLE {materialized_table_random_name} AS SELECT category,count(category) FROM {stream_name_random} GROUP BY category EMIT CHANGES;",
stream_properties={"ksql.streams.auto.offset.reset": "earliest"},)

query_res = client.ksql("LIST TABLES;")
table_names = [table['name'] for table in query_res[0]['tables']]

if materialized_table_random_name in table_names:
    print("Materialized table created")
else:
    print("Table not created")
    exit(1)

# Wait for the data to be handled
print(client.ksql(f"describe {materialized_table_random_name} extended;"))

#Trigger partition update
table_has_data = False
for i in range(timeout):
    des = client.ksql(f"describe {materialized_table_random_name} extended;")
    offset = des[0]['sourceDescription']['queryOffsetSummaries'][0]['topicSummaries']
    if len(offset) != 0:
        print(offset[0]['offsets'])
        table_has_data = True
        break
    else:
        print("No data yet")
    time.sleep(1)

if not table_has_data:
    print(f"Table did not get data after {timeout} seconds")
    exit(1)
try:
    # Query the table
    query_res = client.query(
    f"SELECT * FROM {materialized_table_random_name} WHERE category='test';", use_http2=True, return_objects=True, idle_timeout=30)
    # Get metadata and result
    res = next(query_res)
    res = next(query_res)
    print(f"Got result {res}")
except Exception as e:
    print(f"Query did not succeed {e}")
    exit(1)


