#!/bin/bash
# Usage: connect.sh
# While the SSH Tunnel is open, you can login to clearml from your web browser at http://localhost:8080

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
trap cleanup SIGKILL
trap cleanup SIGSTOP

OPTIONS="-o ServerAliveInterval=10 -o ServerAliveCountMax=60"

# Function to establish an autossh tunnel, retrying on monitor port conflicts
establish_tunnel() {
    local monitor_port=$1
    local forward_port=$2
    local target_port=$3
    local cloud_space_id=$4
    local options=$5
    local output_pipe=$6

    (
        echo "Starting tunnel from $forward_port to $target_port using monitor port $monitor_port..."
        while true; do
            # Try to establish the autossh tunnel and capture the output to check for errors
            # Check for specific message indicating the monitor port is in use
            if check_port $monitor_port; then
                # output=$(autossh -4 -M $monitor_port -N -L $forward_port:0.0.0.0:$target_port $options s_${cloud_space_id}@ssh.lightning.ai 2>&1)
                # echo "$output"
                echo "Starting tunnel from $forward_port to $target_port using monitor port $monitor_port..."
                autossh -4 -M $monitor_port -N -L $forward_port:0.0.0.0:$target_port $options s_${cloud_space_id}@ssh.lightning.ai &
                autossh_pid=$!
                wait $autossh_pid
                # echo "Monitor port $monitor_port in use, trying next available port..."
                # ((monitor_port++))  # Increment monitor port to find a free one
            else
                echo "Monitor port $monitor_port in use, trying next available port..."
                ((monitor_port++))
            fi
        done
    ) > $output_pipe &
}

# Create a FIFO for output
rm -f /tmp/output_pipe
mkfifo /tmp/output_pipe
# Open the FIFO for reading in the background and redirect its contents to stdout
cat /tmp/output_pipe &

ssh -T s_${CLEARML_LIGHTNING_CLOUD_SPACE_ID}@ssh.lightning.ai &

# Kill initial SSH session
pkill -f "ssh s_${CLEARML_LIGHTNING_CLOUD_SPACE_ID}@ssh.lightning.ai"

# Set a random starting point within the dynamic port range for the monitor port
BASE_MONITOR_PORT=$((49152 + $(python -c 'import random; print(random.randint(0,16384))')))

# Establish tunnels with retries on monitor port conflicts, directing output to FIFO
establish_tunnel $BASE_MONITOR_PORT 8080 8080 $TARGET_LIGHTNING_ID "$OPTIONS" /tmp/output_pipe
BASE_MONITOR_PORT=$(($BASE_MONITOR_PORT + 1))
establish_tunnel $BASE_MONITOR_PORT 8008 8008 $TARGET_LIGHTNING_ID "$OPTIONS" /tmp/output_pipe
BASE_MONITOR_PORT=$(($BASE_MONITOR_PORT + 1))
establish_tunnel $BASE_MONITOR_PORT 8081 8081 $TARGET_LIGHTNING_ID "$OPTIONS" /tmp/output_pipe

# Wait a bit for tunnels to establish
sleep 2
echo "SSH tunnels established. Press Ctrl-C to terminate." > /tmp/output_pipe

# Clean up
wait
rm /tmp/output_pipe


# Wait indefinitely to keep the script running
while true; do
    sleep 1
done
