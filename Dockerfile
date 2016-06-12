FROM ubuntu:16.04

MAINTAINER DongWeiming <ciici123@gmail.com>
ENV DEBIAN_FRONTEND noninteractive

RUN echo 'deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse\n\
    deb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse\n\
    deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse\n\
    deb http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse\n\
    deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse\n\
    ' > /etc/apt/sources.list

RUN apt-get update
RUN apt-get install python curl git zsh sudo -yq
RUN useradd -ms /bin/bash ubuntu
RUN echo "ubuntu ALL=(ALL) NOPASSWD: ALL"  >> /etc/sudoers
RUN echo "ubuntu:ubuntu" | chpasswd
USER ubuntu
workdir /home/ubuntu
RUN git clone https://github.com/dongweiming/web_develop
RUN cd /home/ubuntu/web_develop

EXPOSE 9000 3141 22 5000