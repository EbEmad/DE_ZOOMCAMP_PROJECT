FROM bitnami/kafka:3.7

USER root

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install --no-cache-dir \
    pandas==2.2.1 \
    kafka-python==2.0.2 \
    numpy==1.26.4 \
    apache-airflow-providers-apache-kafka==1.3.0

COPY create-topics.sh /create-topics.sh
RUN chmod +x /create-topics.sh

USER 1001
