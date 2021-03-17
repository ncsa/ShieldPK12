#!/bin/sh

BRANCH=develop
git checkout $BRANCH

OLD_HEAD=$(git rev-parse HEAD)
git pull origin $BRANCH
NEW_HEAD=$(git rev-parse HEAD)

if [ $OLD_HEAD = $NEW_HEAD ]; then
    echo $(date) "Up-to-date"
else
    echo $(date) "Need to redeploy"
    docker-compose down
    docker-compose up --build -d
fi
