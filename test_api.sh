#!/bin/bash
# RAG API - Example curl requests
# Use these to test your running server

BASE_URL="http://localhost:8000"

echo "======================================"
echo "RAG API - Testing Curl Commands"
echo "======================================"
echo ""

# Health Check
echo "1. Health Check"
echo "$ curl $BASE_URL/health"
curl -s "$BASE_URL/health" | jq .
echo ""

# Root Info
echo "2. API Info"
echo "$ curl $BASE_URL/"
curl -s "$BASE_URL/" | jq .
echo ""

# Example Question 1
echo "3. Example Query 1"
echo '$ curl -X POST '"$BASE_URL"'/ask -H "Content-Type: application/json" -d '"'"'{"question": "What are the main topics?"}'"'"
curl -s -X POST "$BASE_URL/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the main topics?"}' | jq .
echo ""

# Example Question 2
echo "4. Example Query 2"
echo '$ curl -X POST '"$BASE_URL"'/ask -H "Content-Type: application/json" -d '"'"'{"question": "How does this work?"}'"'"
curl -s -X POST "$BASE_URL/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "How does this work?"}' | jq .
echo ""

# Invalid Request (too short)
echo "5. Validation Error - Empty Question"
echo '$ curl -X POST '"$BASE_URL"'/ask -H "Content-Type: application/json" -d '"'"'{"question": ""}'"'"
curl -s -X POST "$BASE_URL/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": ""}' | jq .
echo ""

echo "======================================"
echo "Individual curl commands to copy-paste:"
echo "======================================"
echo ""

cat << 'EOF'
# Health check
curl http://localhost:8000/health

# Simple question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this about?"}'

# Question with special characters
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the pros and cons?"}'

# Pretty-printed response
curl -s -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Summarize the main findings"}' | jq '.answer' -r

# Save response to file
curl -s -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What do you recommend?"}' | jq . > response.json

# Test with timeout (5 seconds)
curl --max-time 5 -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Your question"}'

EOF

echo ""
echo "======================================"
echo "Testing complete!"
echo "======================================"
