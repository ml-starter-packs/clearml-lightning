#!/bin/bash

# Check if the user provided an argument
if [ "$#" -lt 1 ]; then
            echo "Usage: $0 <number_of_replicas> <queues>"
                exit 1
fi

# Number of replicas
REPLICAS=${1:-1}
CLEARML_AGENT_QUEUES="${2:-scale}"

# Generate the Docker Compose file with a template for worker settings
cat <<EOF > compose.yml
x-worker_template: &worker_defaults
  image: worker
  cpu_count: 1
  deploy:
    restart_policy:
      condition: unless-stopped
  privileged: false
  env_file: .env
  network_mode: host
  # volumes:
  #   - ./entrypoint.sh:/home/agent/entrypoint.sh
  entrypoint: >
    bash -c "curl --retry 10 --retry-delay 2 --retry-connrefused 'http://0.0.0.0:8008/debug.ping' && /home/agent/entrypoint.sh"


services:
EOF

# Append each service configuration using the template
for (( i=1; i<=REPLICAS; i++ )); do
  INDEX=$(printf "%03d" $i)
  cat <<EOF >> compose.yml
  worker_$INDEX:
    <<: *worker_defaults
    container_name: worker$INDEX
    environment:
      CLEARML_WORKER_ID: "A$INDEX-s_${LIGHTNING_CLOUD_APP_ID:-$HOSTNAME}"

EOF

done

echo "Docker Compose file with $REPLICAS replicas generated as 'compose.yml'"