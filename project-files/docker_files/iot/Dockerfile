FROM alpine:latest

ARG app_name

ARG app_port

ARG ssh_user

ARG ssh_password

ARG vulnerable_iot_objects

ENV app_port 80

ENV app_name $app_name

ENV ssh_user $ssh_user

ENV ssh_password $ssh_password

COPY ./app /app/

COPY set-telnet-root.sh /

COPY init.sh /

COPY ./supervisord.conf /etc/supervisord.conf

COPY ./requirements.txt /tmp/requirements.txt

RUN apk update \
    && apk add --no-cache curl bash nano openssh openrc supervisor python3 tmux wget \
    && python3 -m ensurepip \
    && rm -r /usr/lib/python*/ensurepip \
    && pip3 install --upgrade pip setuptools -qr /tmp/requirements.txt \
    && sed -i "s/porta/$app_port/g" /etc/supervisord.conf \
    && rm -r /root/.cache \
    && rm -rf /tmp/* /var/cache/apk/* \
    && sed -i s/#PermitRootLogin.*/PermitRootLogin\ yes/ /etc/ssh/sshd_config \
    && echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config \
    && echo "UserKnownHostsFile=/dev/null" >> /etc/ssh/ssh_config \
    && echo "$ssh_user:$ssh_password" | chpasswd \
    && ssh-keygen -A \
    && chmod +x /set-telnet-root.sh \
    && chmod +x /init.sh \
    && bash set-telnet-root.sh $app_name $vulnerable_iot_objects

EXPOSE $app_port 22 23

CMD bash -C '/init.sh'
