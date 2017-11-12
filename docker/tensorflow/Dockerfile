# clang c++ developer enviroment
# docker build -t mylinux .

FROM ubuntu:xenial

MAINTAINER heming keh <heming.keh@gmail.com>

RUN set -ex; \
	sed -i -e "s/archive\.ubuntu\.com/mirrors\.aliyun\.com/" /etc/apt/sources.list; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		python3 python3-pip python3-dev; \
	mkdir -p ~/.pip; \
	echo "[global]" >> ~/.pip/pip.conf; \
	echo "index-url = http://mirrors.aliyun.com/pypi/simple/" >> ~/.pip/pip.conf; \
	echo "" >> ~/.pip/pip.conf; \
	echo "[install]" >> ~/.pip/pip.conf; \
	echo "trusted-host=mirrors.aliyun.com" >> ~/.pip/pip.conf; \
	pip3 install --upgrade pip; \
	pip3 install setuptools; \
	pip3 install numpy tensorflow; \
	rm -rf /var/lib/apt/lists/*


