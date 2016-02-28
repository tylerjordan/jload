FROM juniper/pyez:latest

MAINTAINER ntwrkguru@gmail.com

ENV DEBIAN_FRONTEND noninteractive

RUN gpt-get install -y git \
&& git clone https://github.com/tylerjordan/jload.git
