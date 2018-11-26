# 介绍

1. [官网](https://termux.com/)
2. [wiki](https://wiki.termux.com/wiki/Main_Page)
3. [github](https://github.com/termux)

# ubuntu

## reinstall to include man pages

    dpkg -l | grep ^ii | cut -d' ' -f3 | xargs apt-get install -y --reinstall && \
    rm -r /var/lib/apt/lists/*

## vim

    git clone --depth 1 --recursive --shallow-submodules \
    https://github.com/heming-keh/vim-pathogen.git ~/.vim

## python

scipy和numpy等一些软件包涉及底层硬件相关的一些编译，所以只能通过apt来安装。

    apt install --no-install-recommends python3 python3-scipy python3-numpy python3-matplotlib
    pip install setuptools wheel
    pip install ipython sphinx


## texlive

    apt install --no-install-recommends texlive texlive-xelatex texlive-lang-cjk texlive-lang-chinese
    apt install --no-install-recommends graphviz

