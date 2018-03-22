#!/usr/bin/env bash

redis-server &
mongod &

pip3 install -r requirement.txt

cd news_pipeline
python3 news_monitor.py &
python3 news_fetcher.py &
python3 news_deduper.py &

echo "=========================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESS." PRESSKEY

redis-cli shutdown
kill $(jobs -p)