FROM juniper/pyez:alpine

MAINTAINER ntwrkguru@gmail.com

RUN apk update && apk add git \
&& git clone https://github.com/tylerjordan/jload.git
