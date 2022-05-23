#!/bin/bash
set -e

./scripts/install_kubectl.sh
pip install ksql

./scripts/wait_for_pod.sh ksqldb-0
python /scripts/python_ksql.py http://ksqldb:8088 
