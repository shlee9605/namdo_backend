#!/bin/bash

# setting - docker info
DOCKER_USER_NAME=wolfandcamel
DOCKER_IMAGE_NAME=namdo_backend
DOCKER_IMAGE_TAG=1.0
DOCKER_CONTAINER_NAME=namdoBack
DOCKER_PORT1=3000
DOCKER_PORT2=8000
DOCKER_VOLUME=/home/docker/volumes/$DOCKER_CONTAINER_NAME
DOCKER_IMAGE=$DOCKER_USER_NAME/$DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG

# docker run #################################
docker run --name $DOCKER_CONTAINER_NAME \
        -p $DOCKER_PORT1:3000 \
        -p $DOCKER_PORT2:8000 \
        --env-file=.env \
        -d \
        $DOCKER_IMAGE