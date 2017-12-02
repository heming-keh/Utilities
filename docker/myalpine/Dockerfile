# docker build -t myalpine .

FROM alpine:3.7

MAINTAINER heming keh <heming.keh@gmail.com>

RUN set -ex; \
	sed -i -e "s/^/#/" /etc/apk/repositories; \
	echo "http://mirrors.aliyun.com/alpine/v3.7/main" >> /etc/apk/repositories; \
	echo "http://mirrors.aliyun.com/alpine/v3.7/community" >> /etc/apk/repositories; 

