#!/usr/bin/env bash

echo " init the airflow daatbase..."

airflow db init

echo " creating admin user...."

airflow users create \
        --username admin \
        --firstname Ebrahim \
        --lastname Emad \
        --role Admin \
        --email admin@example.com \
        --password admin
echo "Starting $1..."
exec airflow "$1"