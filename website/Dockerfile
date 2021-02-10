# Dockerfile
# Pull base image
FROM python:3.9.1

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Add requirements to docker container
ADD ./requirements.txt /requirements.txt
# Install the dependencies
RUN pip install -r requirements.txt

# Set the working directory to /app
WORKDIR /app
# Add content
ADD . /app