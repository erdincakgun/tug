kdec() {
  if [ -z "$1" ]; then
    echo "Usage: kdec <secret-name>"
    return 1
  fi
  local secret_name=$1
  kubectl get secret "$secret_name" -o json | jq '.data |= map_values(@base64d)' | yq e -P
}

kprune() {
  notRunningPods=$(kubectl get pods -A | grep Completed)
  echo "$notRunningPods" | while read -r line; do
    namespace=$(echo "$line" | awk '{print $1}')
    pod=$(echo "$line" | awk '{print $2}')
    kubectl delete pod "$pod" -n "$namespace"
  done
}