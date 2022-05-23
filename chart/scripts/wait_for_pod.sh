name=$1
pod=0
i=0
pod_count=0
echo "Waitin for pod $name"
# Wait for the pod to exist
while ([ 0 -eq $pod_count ] && [ $i -le 120 ]); do
    i=$(($i + 1))
    echo "Waiting for Kafka pod to exist: '$1'"
    kubectl get pods -A
    pod_count=$(kubectl get pods --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}' | grep $name -c)
    sleep 5     
done

if [ 1 -eq $pod_count ]
then
    echo "Found pod $name"
    name=$(kubectl get pods --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}' | grep $name) 
else
    exit 1
fi 

# Wait for the pod to be in running state
while ([ 0 -eq $pod ] && [ $i -le 120 ]); do
    i=$(($i + 1))
    echo "Waiting for Kafka pod to be in state Running"
    kubectl describe pod $name
    pod=$(kubectl get pods -A | grep $name | grep Running -c)
    sleep 5   
done
if [ 1 -eq $pod ]
then
    echo "Found Kafka pod: $name"
    kubectl get pods -A
    kubectl get svc
else
    echo "No pod found with name: $name"
fi

