#!/usr/bin/env bash

source ./env/bin/activate
if [[ -n $(lsof -Pi :8000 -sTCP:LISTEN -t) ]]; then
	echo ""
	echo "WARNING: Port 8000 is in use!"
	echo ""
	echo "Please close any server running on port 8000!"
	echo ""
	echo "must be able to run our servers on 8000"
	echo ""
	read -p "Press enter to continue"
fi

python3 manage.py runserver &
CONTENT_SERVER_PID=$!

sleep 5

curl -0 http://localhost:8000/download/outside_temp.txt -O
curl -0 http://localhost:8000/download/hi_temp.txt -O
curl -0 http://localhost:8000/download/forecast.txt -O

kill $(lsof -t -i:8000)
