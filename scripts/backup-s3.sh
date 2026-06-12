#!/bin/bash
set -euo pipefail

BUCKET="s3://cartflow-logs-backup"
LOG_DIR="/var/log/cartflow"
ARCHIVE="/tmp/cartflow-logs-$(date +%Y%m%d).tar.gz"

echo "Starting backup: $(date)"
tar -czf "$ARCHIVE" "$LOG_DIR" 2>/dev/null || true
aws s3 cp "$ARCHIVE" "$BUCKET/" --sse AES256
rm -f "$ARCHIVE"
echo "Backup complete: $(date)"
