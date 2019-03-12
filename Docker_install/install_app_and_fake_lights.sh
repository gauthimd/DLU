#!/usr/bin/env bash

docker stop docklights-run
docker rm docklights-run
docker build -f Dockerfile_app -t docklights ..
docker run --name docklights-run -p 80:80 -v /home/db:/home/db -d docklights
docker stop fake-lights-run
docker rm fake-lights-run
docker build -f Dockerfile_fake_lights -t fake-lights ..
docker run --name fake-lights-run -v /home/db:/home/db -d fake-lights
