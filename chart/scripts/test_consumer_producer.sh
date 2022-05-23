#!/bin/bash
set -e

./scripts/install_kubectl.sh
pip install kafka-python

./scripts/wait_for_pod.sh kafka-0
python /scripts/python_producer.py kafka topic-test-1
python /scripts/python_consumer.py kafka topic-test-1 10
