# Description: Dockerfile to build a container with Terraform installed
FROM ubuntu:latest

# use root user to run commands
USER root

# Update and install dependencies
RUN apt-get update && apt-get install -y wget unzip


WORKDIR /terraform

COPY /terraform/ /terraform/

# Download and install Terraform
RUN wget https://releases.hashicorp.com/terraform/1.5.0/terraform_1.5.0_linux_amd64.zip \
    && unzip terraform_1.5.0_linux_amd64.zip \
    && mv terraform /usr/local/bin/ \
    && rm terraform_1.5.0_linux_amd64.zip

CMD ["sleep", "infinity"]