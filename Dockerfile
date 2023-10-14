FROM nikolaik/python-nodejs:python3.10-nodejs17
RUN apt-get update && apt-get upgrade -y
RUN apt install redis-server -y
RUN pip3 install -r requirements.txt
COPY . /app/
WORKDIR /app/
CMD python3 main.py