#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5003"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done


###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to check the database connection
check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}

#smoketest test

create_boxer() {
  name=$1
  weight=$2
  height=$3
  reach=$4
  age=$5

  echo "Creating boxer: $name"
  response=$(curl -s -X POST "$BASE_URL/boxers" -H "Content-Type: application/json" \
    -d "{\"name\":\"$name\", \"weight\":$weight, \"height\":$height, \"reach\":$reach, \"age\":$age}")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "PASS: Boxer '$name' created."
  else
    echo "FAIL: Failed to create boxer '$name'."
    echo "$response"
    exit 1
  fi
}


create_boxer "Ali" 145 69 72.0 29

echo "Smoketest completed."