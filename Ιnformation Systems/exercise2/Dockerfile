FROM ubuntu:16.04
RUN apt update && apt install -y python3-pip
RUN pip3 install requests
RUN mkdir /script
COPY ex2.py /script
ENTRYPOINT ["python3","-u","/script/ex2.py"]