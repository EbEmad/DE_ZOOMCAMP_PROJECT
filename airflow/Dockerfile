FROM apache/airflow:2.10.4

USER root

RUN groupadd docker && usermod -aG docker airflow

COPY requirements.txt /requirements.txt
COPY Airflow.sh /run.sh
RUN chmod +x /run.sh

USER airflow

RUN pip install -r /requirements.txt

CMD ["bash", "/run.sh"]
