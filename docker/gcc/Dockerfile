# clang c++ developer enviroment
# docker build -t mylinux .

FROM ubuntu:xenial

MAINTAINER heming keh <heming.keh@gmail.com>

RUN set -ex; \
	sed -i -e "s/archive\.ubuntu\.com/mirrors\.aliyun\.com/" /etc/apt/sources.list; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		gcc g++ make gdb valgrind; \
	rm -rf /var/lib/apt/lists/*

