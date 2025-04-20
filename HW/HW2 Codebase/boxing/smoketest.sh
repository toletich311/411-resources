#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5003/api"

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

#call health checks
check_health
check_db

###############################################
#
# Boxer tests
#
###############################################

### function defitions
create_boxer() {
  name=$1
  weight=$2
  height=$3
  reach=$4
  age=$5

  echo "Creating boxer: $name"
  response=$(curl -s -X POST "$BASE_URL/add-boxer" -H "Content-Type: application/json" \
    -d "{\"name\":\"$name\", \"weight\":$weight, \"height\":$height, \"reach\":$reach, \"age\":$age}")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "PASS: Boxer '$name' created."
  else
    echo "FAIL: Failed to create boxer '$name'."
    echo "$response"
    exit 1
  fi
}

delete_boxer_by_id(){
  id=$1
  echo "Deleting boxer with ID $id..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-boxer/$id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "PASS: Boxer ID $id deleted"
  else
    echo "FAIL: Failed to delete boxer with ID $id"
    exit 1
  fi
}

clear_all_boxers() {
  echo "Clearing all boxers..."
  response=$(curl -s -X POST "$BASE_URL/clear-boxers")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "PASS: All boxers cleared."
  else
    echo "FAIL: Failed to clear all boxers."
    echo "$response"
    exit 1
  fi
}

get_boxer_by_id(){
   id=$1
  echo "Getting boxer with ID $id..."
  response=$(curl -s "$BASE_URL/get-boxer-by-id/$id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "PASS: Retrieved boxer with ID $id"
    if [ "$ECHO_JSON" = true ]; then
      echo "$response" | jq .
    fi
  else
    echo "FAIL: Failed to retrieve boxer with ID $id"
    exit 1
  fi
}

get_boxer_by_name() {
  name=$1
  echo "Getting boxer with name $name..."
  response=$(curl -s "$BASE_URL/get-boxer-by-name/$name")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "PASS: Retrieved boxer '$name'"
    if [ "$ECHO_JSON" = true ]; then
      echo "$response" | jq .
    fi
  else
    echo "FAIL: Failed to retrieve boxer '$name'"
    echo "$response"
    exit 1
  fi
}

###############################################
#
# Ringmodel Tests
#
###############################################

enter_ring() {
  name=$1
  echo "Adding $name to the ring..."
  response=$(curl -s -X POST "$BASE_URL/enter-ring" \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"$name\"}")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "PASS: $name added to the ring."
  else
    echo "FAIL: Failed to add $name to the ring."
    echo "$response"
    exit 1
  fi
}

start_fight() {
  echo "Triggering a fight..."
  response=$(curl -s -X GET "$BASE_URL/fight")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "PASS: Fight triggered successfully."
  else
    echo "FAIL: Failed to trigger fight."
    echo "$response"
    exit 1
  fi
}

get_leaderboard() {
  echo "Fetching leaderboard..."
  response=$(curl -s "$BASE_URL/leaderboard")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "PASS: Leaderboard retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "$response" | jq .
    fi
  else
    echo "FAIL: Failed to retrieve leaderboard."
    echo "$response"
    exit 1
  fi
}

###############################################
#
# RUNNING SMOKETESTS
#
###############################################

#resetDB
docker exec boxing-app_container /app/sql/create_db.sh

#create valid boxers 
create_boxer "Pacquiao" 190 72 73.0 29
create_boxer "Tyson" 220 70 71.0 28
create_boxer "Holyfield" 210 74 78.0 32

#try to create a duplicate boxer -- this test should fail
# Try to create the same boxer again (should fail)
echo "Trying to create boxer with duplicate name..."
response=$(curl -s -X POST "$BASE_URL/add-boxer" -H "Content-Type: application/json" \
  -d '{"name":"Holyfield", "weight":210, "height":74, "reach":78.0, "age":32}')
if echo "$response" | grep -q '"status": "error"'; then
  echo "PASS: Duplicate boxer name correctly rejected."
else
  echo "FAIL: Duplicate boxer name was not rejected."
  echo "$response"
  exit 1
fi

#test retrieval fucntions
get_boxer_by_name "Pacquiao"
get_boxer_by_name "Tyson"
get_boxer_by_name "Holyfield"
get_boxer_by_id 1
get_boxer_by_id 2
get_boxer_by_id 3

#add boxers to ring
enter_ring "Tyson"
enter_ring "Pacquiao"

#start fight
start_fight

#add second set of boxers to ring
enter_ring "Holyfield"
enter_ring "Pacquiao"

#start fight
start_fight

#add third match of boxers to ring
enter_ring "Holyfield"
enter_ring "Tyson"

#add third boxer to the ring -- should fail 
echo "Testing overfilling the ring..."
# Now try to add a third
response=$(curl -s -X POST "$BASE_URL/enter-ring" \
  -H "Content-Type: application/json" \
  -d '{"name":"Pacquiao"}')
if echo "$response" | grep -q '"status": "error"'; then
  echo "PASS: Third boxer not allowed in ring."
else
  echo "FAIL: Third boxer was allowed in the ring!"
  echo "$response"
  exit 1
fi

#get leaderboard 
get_leaderboard
echo "$response" | jq .

#delete boxers
delete_boxer_by_id 1
delete_boxer_by_id 2


#clearing all remaining boxers (just boxer 3)
clear_all_boxers

echo "Smoketest completed."

