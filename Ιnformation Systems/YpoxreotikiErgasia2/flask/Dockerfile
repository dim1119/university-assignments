FROM ubuntu:18.04
RUN apt update && apt-get install -y python3 python3-pip
RUN pip3 install flask pymongo
RUN mkdir /app
COPY app.py /app/app.py 
WORKDIR /app
ENTRYPOINT [ "python3","-u", "app.py" ]