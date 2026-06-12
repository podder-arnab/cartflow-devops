#!/bin/bash
set -euo pipefail

APP_DIR="/home/ubuntu/cartflow"
LOG_FILE="/var/log/cartflow/deploy.log"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"; }

log "=== CartFlow Deployment Started ==="

# Pull latest code
cd "$APP_DIR"
git pull origin main

# Rebuild and restart containers
docker compose down
docker compose up -d --build

# Wait for app to come up
log "Waiting for services to start..."
sleep 10

# Health check
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/api/health)
if [[ "$HTTP_CODE" != "200" ]]; then
    log "ERROR: Health check failed (got $HTTP_CODE)"
    exit 1
fi

# Cleanup old images
docker image prune -f

log "=== Deployment Complete ==="
