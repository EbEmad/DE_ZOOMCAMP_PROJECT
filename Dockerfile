FROM apache/airflow:2.5.1

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the DAGs directory to the Airflow home directory
COPY dags/ /opt/airflow/dags/

# Copy the entrypoint script
COPY Bashentrypoint.sh /entrypoint.sh

USER root
RUN chmod +x /entrypoint
RUN groupadd docker
RUN usermod -aG docker airflow

USER airflow

ENTRYPOINT [ "/entrypoint.sh" ]
