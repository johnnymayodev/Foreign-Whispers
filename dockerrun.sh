#! /bin/bash

docker stop foreign-whispers
docker rm foreign-whispers
docker build -t foreign-whispers .
docker run --privileged -p 5005:5005 --name foreign-whispers foreign-whispers