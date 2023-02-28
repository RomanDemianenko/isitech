FROM python:3.10
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
  apt-get install -y python3-pip python3-dev

WORKDIR /code
COPY . /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
