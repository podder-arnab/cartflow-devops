#!/bin/bash
ENDPOINT="http://localhost/api/health"
MAX_RETRIES=5

echo "Running CartFlow health check..."

for i in $(seq 1 $MAX_RETRIES); do
    CODE=$(curl -s -o /dev/null -w "%{http_code}" "$ENDPOINT")
    if [[ "$CODE" == "200" ]]; then
        echo "HEALTHY - App is running (attempt $i)"
        exit 0
    fi
    echo "Attempt $i: got HTTP $CODE, retrying in 10s..."
    sleep 10
done

echo "UNHEALTHY - App failed after $MAX_RETRIES attempts"
exit 1
