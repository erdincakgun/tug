kdec() {
  if [ -z "$1" ]; then
    echo "Usage: kdec <secret-name>"
    return 1
  fi
  local secret_name=$1
  kubectl get secret "$secret_name" -o json | jq '.data |= map_values(@base64d)' | yq e -P
}