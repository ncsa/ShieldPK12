#!/bin/sh

BRANCH=develop
git checkout $BRANCH

OLD_HEAD=$(git rev-parse HEAD)
git pull origin $BRANCH
NEW_HEAD=$(git rev-parse HEAD)

if [ $OLD_HEAD = $NEW_HEAD ]; then
    echo $(date) "Up-to-date"
elif [ $LOCAL = $BASE ]; then
    echo $(date) "Need to redeploy"
    docker-compose down
    docker-compose up --build -d
else
    echo $(date) "Diverged"
fi
