FROM ubuntu:xenial

RUN apt-get update \
    && apt-get upgrade -q -y \
    && apt-get dist-upgrade -q -y \
    && apt-get install -q -y wget curl \
    && apt-get install -y python3-pip python3-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip \
    && hash -r pip \
    && pip3 install savoir \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && cd /tmp \
    && wget http://www.multichain.com/download/multichain-1.0.4.tar.gz \
    && tar -xvzf multichain-1.0.4.tar.gz \
    && cd multichain-1.0.4 \
    && mv multichaind multichain-cli multichain-util /usr/local/bin \
    && cd /tmp \
    && rm -Rf multichain*

COPY ./runchain.sh /root/runchain.sh
COPY ./blocknotify.sh /root/blocknotify.sh
RUN chmod a+x /root/runchain.sh
RUN chmod a+x /root/blocknotify.sh

CMD ["/bin/bash", "/root/runchain.sh"]
