# Confluent Kafka
* Entities are HA with port mappings. If we do not have 6 k8s nodes we need to configure rack awareness or affinity for either broker or zookeeper


### How to
https://docs.confluent.io/operator/current/co-quickstart.html#co-quickstart
#### Install CFK
<code>
helm upgrade --install confluent-operator \
  confluentinc/confluent-for-kubernetes \
  --namespace <namespace>
<code>

#### Configure CRs
https://docs.confluent.io/operator/current/co-configure-overview.html#use-kubectl-to-examine-cp-crds

https://github.com/confluentinc/confluent-kubernetes-examples/blob/master/general/cp-version/confluent-platform-7.1.0.yaml
