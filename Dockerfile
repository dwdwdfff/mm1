RUN apt-get update && apt-get upgrade -y
RUN apt install redis-server -y
RUN pip3 install -U pip
RUN pip3 install -U -r requirements.txt
CMD python3 main.py