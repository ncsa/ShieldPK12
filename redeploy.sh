#!/bin/sh

git checkout develop

UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")

if [ $LOCAL = $REMOTE ]; then
    echo $(date) "Up-to-date"
elif [ $LOCAL = $BASE ]; then
    echo $(date) "Need to pull"
    git pull
    docker-compose down
    docker-compose up --build -d
else
    echo $(date) "Diverged"
fi
