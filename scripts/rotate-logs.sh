#!/bin/bash
LOG_DIR="/var/log/cartflow"

echo "Rotating logs: $(date)"
find "$LOG_DIR" -name "*.log" -mtime +7 -exec gzip {} \;
find "$LOG_DIR" -name "*.gz" -mtime +30 -delete
echo "Log rotation complete: $(date)"
