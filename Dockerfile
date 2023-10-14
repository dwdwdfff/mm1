FROM python:3.9.7-slim-buster
RUN apt-get update && apt-get upgrade -y
RUN apt install redis-server -y
RUN pip3 install -U pip
RUN pip3 install -U -r requirements.txt
COPY . /app/
WORKDIR /app/
CMD python3 main.py