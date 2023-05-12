ARG CORE_IMAGE
FROM ${CORE_IMAGE}

WORKDIR /root/app
COPY ./app/app.py .

COPY ./build/app/entrypoint.sh /usr/bin/entrypoint.sh
ENTRYPOINT sh /usr/bin/entrypoint.sh
