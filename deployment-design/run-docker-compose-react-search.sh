#!/bin/bash

# chmod +x run-docker-compose-react-search.sh

# run from deployment-design folder: ./run-docker-compose-react-search.sh
# or run from deployment-design folder:
#   docker-compose.yaml build
#   docker compose up -d

docker-compose -f docker-compose.yaml build
docker-compose -f docker-compose.yaml up -d
