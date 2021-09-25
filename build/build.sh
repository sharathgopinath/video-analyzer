#!/usr/bin/env bash
set -euxo pipefail

: ${GIT_SHA?"GIT_SHA env variable is required"}

project="video-analyzer"

cleanup() {
    echo "Cleaning up ..."
    docker-compose \
      -p ${project} \
      -f ../docker-compose.tests.yml \
      -f ../docker-compose.yml down \
      --remove-orphans || true
      
    docker stop $(docker ps -a -q) || true
    docker rm $(docker ps -a -q) || true
    docker image rm "${project}:${GIT_SHA}" || true
}

echo "Create package..."

mkdir ./packages || true

cp -a ../video_analyzer/. ./packages
pip install -r ../requirements.txt -t ./packages

cleanup

echo "Running tests..."
docker-compose -f ../docker-compose.yml -f ../docker-compose.tests.yml pull
docker-compose \
  -p ${project} \
  -f ../docker-compose.yml  \
  -f ../docker-compose.tests.yml \
  up \
  --build --force-recreate --remove-orphans \
  --exit-code-from tests \
  --abort-on-container-exit \
  tests

aws cloudformation package \
    --template-file="./cloudformation.yaml" \
    --output-template-file="./package.yaml" \
    --s3-prefix="${project}/${GIT_SHA}" \
    --s3-bucket="my-aws-code"

aws s3 cp "./package.yaml" "s3://my-aws-code/${project}/${GIT_SHA}/"