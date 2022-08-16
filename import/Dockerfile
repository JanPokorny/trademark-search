FROM alpine:3.16

RUN apk add --no-cache \
        aria2 \
        jq \
        parallel \
        postgresql14-client \
        python3 \
        py3-pip \
        unzip \
    && \
    pip3 install --no-cache-dir \
         yq

WORKDIR /workdir
COPY . .
RUN chmod +x ./import.sh

VOLUME /workdir/data
