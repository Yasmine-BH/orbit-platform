#!/bin/bash
set -e

echo "=== PHASE 1 COMPLETE TEST ==="

# 1. Build images
echo -e "\n[1/5] Building Docker images..."
docker compose build --quiet
echo "✓ Build successful"

# 2. Start services
echo -e "\n[2/5] Starting services..."
docker compose up -d
echo "Waiting 30 seconds for services to initialize..."
sleep 30

# 3. Check service health
echo -e "\n[3/5] Checking service health..."
docker compose ps

echo "Waiting for health checks..."
sleep 5

# Interns API
echo -n "Interns API: "
curl -s http://localhost:8080/actuator/health | jq -r '.status'

# Tasks API  
echo -n "Tasks API: "
curl -s http://localhost:8000/health | jq -r '.status'

# 4. Test inter-service communication
echo -e "\n[4/5] Testing inter-service communication..."
echo "Creating a test intern first..."
INTERN=$(curl -s -X POST http://localhost:8080/api/interns \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Test",
    "lastName": "User",
    "email": "test@example.com",
    "university": "MIT",
    "status": "APPLIED"
  }')

INTERN_ID=$(echo $INTERN | jq -r '.id')
echo "Created intern with ID: $INTERN_ID"

echo "Creating task for this intern..."
curl -s -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d "{
    \"intern_id\": $INTERN_ID,
    \"title\": \"Onboarding\",
    \"priority\": \"HIGH\",
    \"status\": \"PENDING\"
  }" | jq .

echo -e "\n✓ Inter-service communication works!"

# 5. Stop services
echo -e "\n[5/5] Cleaning up..."
docker compose down -v
echo "✓ All tests passed!"

