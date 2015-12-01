#!/usr/bin/env python

import os
import sys
import urllib

if sys.platform == 'win32':
    sys.exit(1)

home = '/home/vagrant'
ubuntu_code = 'trusty'


######################################################################
# apt-get source.list
######################################################################
print('/etc/apt/sources.list')
sources_list_backup = '/etc/apt/sources.list.backup'
sources_list = '/etc/apt/sources.list'
# backup
if not os.path.exists(sources_list_backup) and os.path.isfile(sources_list):
    os.rename(sources_list, sources_list_backup)
# write sources.list
mirror = 'http://mirrors.aliyun.com/ubuntu/'
with open(sources_list, 'w') as f:
    f.write(
        'deb {mirror} {ubuntu_code} main restricted universe multiverse\n'
        'deb {mirror} {ubuntu_code}-security main restricted universe multiverse\n'
        'deb {mirror} {ubuntu_code}-updates main restricted universe multiverse\n' 
        'deb {mirror} {ubuntu_code}-proposed main restricted universe multiverse\n'
        'deb {mirror} {ubuntu_code}-backports main restricted universe multiverse\n'
        'deb-src {mirror} {ubuntu_code} main restricted universe multiverse\n'
        'deb-src {mirror} {ubuntu_code}-security main restricted universe multiverse\n'
        'deb-src {mirror} {ubuntu_code}-updates main restricted universe multiverse\n'
        'deb-src {mirror} {ubuntu_code}-proposed main restricted universe multiverse\n'
        'deb-src {mirror} {ubuntu_code}-backports main restricted universe multiverse\n'
        .format(ubuntu_code=ubuntu_code, mirror=mirror)
    )



######################################################################
# pip mirror
######################################################################
print('Python pip')
pip_dir = os.path.join(home, '.pip')
if not os.path.exists(pip_dir):
    os.makedirs(pip_dir)
with open(os.path.join(pip_dir, 'pip.conf'), 'w') as f:
    f.write('[global]\n'
            'index-url = http://mirrors.aliyun.com/pypi/simple/\n')



######################################################################
# git
######################################################################
print('GIT')
with open(os.path.join(home, '.gitconfig'), 'w') as f:
    f.write('[user]\n'
            'email = heming.keh@gmail.com\n'
            'name = heming_keh\n')


######################################################################
# vim
######################################################################
print('VIM')
vim_pathogen = 'https://raw.githubusercontent.com/tpope/vim-pathogen/master/autoload/pathogen.vim'
print('retrieve {}'.format(vim_pathogen))
vim_autoload_dir = os.path.join(home, '.vim/autoload')
if not os.path.exists(vim_autoload_dir):
    os.makedirs(vim_autoload_dir)
urllib.urlretrieve(vim_pathogen, os.path.join(vim_autoload_dir, 'pathogen.vim'))

with open(os.path.join(home, '.vimrc'), 'w') as f:
    f.write('source /mnt/D/Vimrc/_vimrc')



######################################################################
# commands
######################################################################
os.system('sudo apt-get update')
os.system('sudo apt-get -y install vim')
os.system('sudo apt-get -y install git')


######################################################################
# hostname
######################################################################
with open('/etc/hostname', 'w') as f:
    f.write('trusty')
