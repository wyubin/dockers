FROM alpine:3.4
RUN apk update && \
  apk add --no-cache -U nginx supervisor python py-pip sqlite \
  ## for python packages
  libc-dev gcc linux-headers python-dev geoip-dev
## python packages
RUN pip install -U flask uwsgi peewee GeoIP validate_email biopython==1.76 numpy==1.16.1

## copy src
COPY settings /settings
COPY nginx /nginx
COPY uwsgi /uwsgi

## prepare env
RUN ln -fs /nginx/default.conf /etc/nginx/conf.d/default.conf &&\
    ln -fs /nginx/nginx.conf /etc/nginx/nginx.conf

## make user
RUN adduser -D -G www-data www-data

#RUN addgroup www-data && adduser -g www-data www-data
