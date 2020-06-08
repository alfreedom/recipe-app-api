FROM python:3.7-alpine
MAINTAINER Alfredo Orozco de la Paz

# Set Python Unbuffered 1 to avoid standar output buffered.
ENV PYTHOUNBUFFERED 1

# Needed by pyscopg-binary
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

# Copy the requirementes to the container and install it
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Clear the temp build dir
RUN apk del .tmp-build-deps

# Make the app directory and set as work directory
RUN mkdir /app
WORKDIR /app

# Copy the code to the work directory
COPY ./app /app

# Add user for the app
RUN adduser -D app_user

# Set the contaner user to the user app
USER app_user

