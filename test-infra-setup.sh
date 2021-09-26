#!/usr/bin/env bash
set -euxo pipefail

alias aws=/usr/local/aws-cli/v2/current/bin/aws

echo "Waiting for localstack..."
until aws --endpoint-url=http://localstack:4566 dynamodb list-tables; do sleep 2; done
echo "Ready"