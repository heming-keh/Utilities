# clang c++ developer enviroment
# docker build -t mylinux .

FROM ubuntu:xenial

MAINTAINER heming keh <heming.keh@gmail.com>

RUN sed -i -e "s/archive\.ubuntu\.com/mirrors\.aliyun\.com/" /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y gcc g++ gdb valgrind
