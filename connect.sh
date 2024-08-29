#!/bin/bash +x

# Function to clean up background jobs
cleanup() {
    echo "Terminating SSH tunnels..."
    pkill -P $$
    echo "All tunnels closed."
    exit 0
}

# Trap Ctrl-C (SIGINT) and call the cleanup function
trap cleanup SIGINT

# SSH options for connection robustness
OPTIONS="-o ServerAliveInterval=30 -o ServerAliveCountMax=5"

# Function to establish an SSH tunnel
establish_tunnel() {
    local forward_port=$1
    local target_port=$2
    local cloud_space_id=$3

    while true; do
        echo "Starting tunnel from $forward_port to $target_port..."
        ssh -N -L $forward_port:0.0.0.0:$target_port $OPTIONS s_${cloud_space_id}@ssh.lightning.ai
        echo "Tunnel from $forward_port to $target_port died. Retrying..."
        sleep 5  # Wait before retrying
    done
}

# Establish a single tunnel shared by all containers on the machine
establish_tunnel 8080 8080 $TARGET_LIGHTNING_ID &
establish_tunnel 8008 8008 $TARGET_LIGHTNING_ID &
establish_tunnel 8081 8081 $TARGET_LIGHTNING_ID &

# Wait a bit for tunnels to establish
sleep 2
echo "SSH tunnels established. Press Ctrl-C to terminate."

# Wait indefinitely to keep the script running
while true; do
    sleep 1
done
