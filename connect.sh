#!/bin/bash
# Usage: connect.sh 

# Function to clean up background jobs
cleanup() {
    echo "Terminating SSH tunnels..."
    kill -- -$$
    echo "All tunnels closed."
    exit 0
}

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -i :$port &>/dev/null; then
        echo "Error: Port $port is already in use."
        exit 1
    fi
}

# Trap Ctrl-C (SIGINT) and call the cleanup function
trap cleanup SIGINT

# Set monitoring ports for autossh
MONITOR_PORT_1=21020
MONITOR_PORT_2=21030
MONITOR_PORT_3=21040

# Check if ports are free
check_port 8080
check_port 8008
check_port 8081
check_port $MONITOR_PORT_1
check_port $MONITOR_PORT_2
check_port $MONITOR_PORT_3

# Start autossh tunnels in the background
autossh -M $MONITOR_PORT_1 -N -L 8080:localhost:8080 s_${LIGHTNING_CLOUD_SPACE_ID}@ssh.lightning.ai &
AUTOSSH_PID_1=$!

autossh -M $MONITOR_PORT_2 -N -L 8008:localhost:8008 s_${LIGHTNING_CLOUD_SPACE_ID}@ssh.lightning.ai &
AUTOSSH_PID_2=$!

autossh -M $MONITOR_PORT_3 -N -L 8081:localhost:8081 s_${LIGHTNING_CLOUD_SPACE_ID}@ssh.lightning.ai &
AUTOSSH_PID_3=$!

echo "SSH tunnels established. Press Ctrl-C to terminate."

# Wait indefinitely to keep the script running
while true; do
    sleep 1
done

