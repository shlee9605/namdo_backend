#!/bin/bash
DOCKER_USER_NAME=wolfandcamel
DOCKER_IMAGE_NAME=namdo_backend
DOCKER_IMAGE_TAG=1.8

docker build -t $DOCKER_USER_NAME/$DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG .