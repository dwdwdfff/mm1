FROM python3.10
RUN apt install redis-server -y
RUN pip3 install -r requirements.txt
COPY . /app/
WORKDIR /app/
CMD python3 main.py