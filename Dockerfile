FROM python:3.8-slim-buster
WORKDIR /algorithm
ADD . /algorithm
RUN pip install -r requirements.txt