FROM tensorflow/tensorflow:1.11.0-devel-gpu-py3

MAINTAINER Nikola Vukobrat

# Pre configuratin system deps
RUN apt-get update -y
RUN apt-get install -y --no-install-recommends apt-utils

# Configure debconf
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# Install locales and gen UTF-8
RUN apt-get update --fix-missing
RUN apt-get install locales
RUN locale-gen en_US.UTF-8

# Set locales env vars
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Update image
RUN apt-get update -y
RUN apt-get upgrade -y

# System deps

# Update python packages
RUN pip install --upgrade pip
RUN pip install pip-review
RUN pip-review --local

# Install python dependencies
RUN pip install pycrypto