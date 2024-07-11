#!/bin/bash

# Function to clean up background jobs
cleanup() {
    echo "Terminating SSH tunnels..."
    kill $AUTOSSH_PID_1 $AUTOSSH_PID_2 $AUTOSSH_PID_3
    wait $AUTOSSH_PID_1 $AUTOSSH_PID_2 $AUTOSSH_PID_3
    echo "All tunnels closed."
    exit 0
}

# Trap Ctrl-C (SIGINT) and call the cleanup function
trap cleanup SIGINT

# Start autossh tunnels in the background
autossh -f -N -L 8080:localhost:8080 s_${LIGHTNING_CLOUD_SPACE_ID}@ssh.lightning.ai &
AUTOSSH_PID_1=$!

autossh -f -N -L 8008:localhost:8008 s_${LIGHTNING_CLOUD_SPACE_ID}@ssh.lightning.ai &
AUTOSSH_PID_2=$!

autossh -f -N -L 8081:localhost:8081 s_${LIGHTNING_CLOUD_SPACE_ID}@ssh.lightning.ai &
AUTOSSH_PID_3=$!

echo "SSH tunnels established. Press Ctrl-C to terminate."

# Wait for background jobs to finish
wait $AUTOSSH_PID_1 $AUTOSSH_PID_2 $AUTOSSH_PID_3
