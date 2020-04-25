FROM ubi8/ubi 

MAINTAINER Paul Needle <paul.needle@gmail.com>

ADD . /var/www/

RUN dnf install -y --setopt=tsflags=nodocs python36 python3-virtualenv && \
    dnf clean all -y && \
    pip3 install Django

EXPOSE 8000

WORKDIR /var/www/counters/

CMD [ "python3", "-u", "manage.py", "runserver", "0.0.0.0:8000"]
