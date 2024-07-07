#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/gunicorn.pid"
NOHUP_FILE="$SCRIPT_DIR/nohup.out"

# check if pid files exists and if it's running for redeployment
if [ -f "$PID_FILE" ]; then
  PID=$(cat "$PID_FILE")
  if ps -p $PID > /dev/null; then
    kill -s QUIT $PID
    sleep 2
  else
    echo "PID file exists but no process found with PID $PID. Removing PID file."
    rm "$PID_FILE"
  fi
else
  echo "PID file not found."
fi

if [ -f "$NOHUP_FILE" ]; then
  rm "$NOHUP_FILE"
fi

# start backend flask app
/usr/bin/nohup gunicorn -w 2 -b 0.0.0.0:8080 -p "$PID_FILE" --timeout 300 run:app &

