FROM juniper/pyez:latest

MAINTAINER ntwrkguru@gmail.com

ENV DEBIAN_FRONTEND noninteractive

RUN git clone https://github.com/tylerjordan/jload.git
