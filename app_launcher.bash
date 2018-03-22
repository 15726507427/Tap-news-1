#!/usr/bin/env bash

redis-server &
mongod &

pip3 install -r requirement.txt

# News Topic Modeling Server
cd ../news_topic_modeling_service/server/
python3 server.py &

# News Recommendation Server
cd ../news_recommendation_service/
python3 recommendation_service.py &

# Click log processor
python3 click_log_processor.py &

# Backend RPC Server
cd backend_server/
python3 service.py &

# Node Server
cd ../web_server/server/
npm install
npm start &

# Frontend
cd ../client/
npm install
npm start
echo Y &

echo "=========================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESS." PRESSKEY

redis-cli shutdown
kill $(jobs -p)