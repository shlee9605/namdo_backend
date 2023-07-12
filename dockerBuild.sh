#!/bin/bash
#docker push wolfandcamel/namdo_backend
DOCKER_USER_NAME=wolfandcamel
DOCKER_IMAGE_NAME=namdo_backend
DOCKER_IMAGE_TAG=2.7

docker build -t $DOCKER_USER_NAME/$DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG .