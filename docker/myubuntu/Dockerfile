# clang c++ developer enviroment
# docker build -t myubuntu .

FROM ubuntu:xenial

MAINTAINER heming keh <heming.keh@gmail.com>

RUN set -ex; \
	sed -i -e "s/archive\.ubuntu\.com/mirrors\.aliyun\.com/" /etc/apt/sources.list; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		gcc g++ make gdb \
		valgrind google-perftools libgoogle-perftools-dev \
		wget iproute2 iputils-ping \
		zip unzip; \
	rm -rf /var/lib/apt/lists/*


# LD_PRELOAD=/usr/lib/libprofiler.so CPUPROFILE=/tmp/profile my_bin_path
