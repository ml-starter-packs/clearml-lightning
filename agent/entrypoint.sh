#!/bin/bash +x

# if TARGET_LIGHTNING_ID is missing, exit
if [ -z "TARGET_LIGHTNING_ID" ]; then
  echo "TARGET_LIGHTNING_ID is missing, exiting"
  exit 1
fi
TARGET_LIGHTNING_ID="${TARGET_LIGHTNING_ID}" /usr/bin/connect

if [ -n "$SHUTDOWN_IF_NO_ACCESS_KEY" ] && [ -z "$CLEARML_API_ACCESS_KEY" ] && [ -z "$TRAINS_API_ACCESS_KEY" ]; then
  echo "CLEARML_API_ACCESS_KEY was not provided, service will not be started"
  exit 0
fi

export CLEARML_FILES_HOST=${CLEARML_FILES_HOST:-$TRAINS_FILES_HOST}

if [ -z "$CLEARML_FILES_HOST" ]; then
    CLEARML_HOST_IP=${CLEARML_HOST_IP:-${TRAINS_HOST_IP:-$(curl -s https://ifconfig.me/ip)}}
fi

export CLEARML_FILES_HOST=${CLEARML_FILES_HOST:-${TRAINS_FILES_HOST:-"http://$CLEARML_HOST_IP:8081"}}
export CLEARML_WEB_HOST=${CLEARML_WEB_HOST:-${TRAINS_WEB_HOST:-"http://$CLEARML_HOST_IP:8080"}}
export CLEARML_API_HOST=${CLEARML_API_HOST:-${TRAINS_API_HOST:-"http://$CLEARML_HOST_IP:8008"}}

echo $CLEARML_FILES_HOST $CLEARML_WEB_HOST $CLEARML_API_HOST 1>&2

if [[ "$CLEARML_AGENT_UPDATE_VERSION" =~ ^[0-9]{1,3}\.[0-9]{1,3}(\.[0-9]{1,3}([a-zA-Z]{1,3}[0-9]{1,3})?)?$ ]]
then
    CLEARML_AGENT_UPDATE_VERSION="==$CLEARML_AGENT_UPDATE_VERSION"
fi

DAEMON_OPTIONS=${CLEARML_AGENT_DAEMON_OPTIONS:---services-mode --create-queue}
QUEUES=${CLEARML_AGENT_QUEUES:-services}

if [ -z "$CLEARML_AGENT_NO_UPDATE" ]; then
  if [ -n "$CLEARML_AGENT_UPDATE_REPO" ]; then
    python3 -m pip install -q -U $CLEARML_AGENT_UPDATE_REPO
  else
    python3 -m pip install -q -U "clearml-agent${CLEARML_AGENT_UPDATE_VERSION:-$TRAINS_AGENT_UPDATE_VERSION}"
  fi
fi

DOCKER_ARGS="--docker \"${CLEARML_AGENT_DEFAULT_BASE_DOCKER:-$TRAINS_AGENT_DEFAULT_BASE_DOCKER}\""

if [ -n "$CLEARML_AGENT_NO_DOCKER" ]; then
  DOCKER_ARGS=""
fi

clearml-agent daemon $DAEMON_OPTIONS --queue $QUEUES $DOCKER_ARGS --cpu-only ${CLEARML_AGENT_EXTRA_ARGS:-$TRAINS_AGENT_EXTRA_ARGS}