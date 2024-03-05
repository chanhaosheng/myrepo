#!/bin/bash

# chmod +x run-docker-compose-asr.sh

# run from asr folder: ./run-docker-compose-asr.sh
# or run from asr folder: docker compose up -d

docker-compose -f docker-compose.yaml build
docker-compose -f docker-compose.yaml up -d
