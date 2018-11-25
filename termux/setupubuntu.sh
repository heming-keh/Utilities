# bash setupubuntu.sh
# requirements: wget tar proot


################################################################################
# settings
################################################################################

# getprop ro.product.cpu.abi
# aarch64 is arm64
ARCH="arm64"
NAME="ubuntu"

ROOTFS_URL="https://partner-images.canonical.com/core/bionic/current/ubuntu-bionic-core-cloudimg-${ARCH}-root.tar.gz"
SHA256SUM_URL="${ROOTFS_URL%/*}/SHA256SUMS"
ROOTFS_FILE=${ROOTFS_URL##*/}
SHA256SUM_FILE=${SHA256SUM_URL##*/}
LINUX_ROOT="${HOME}/.${NAME}"



################################################################################
# create ${LINUX_ROOT}
################################################################################

if [ -d ${LINUX_ROOT} ]; then
  while true; do
    read -p "${NAME} already exists, do you want to delete it? " yn
    case ${yn} in
      [Yy]* )
        for entry in ${LINUX_ROOT}/*; do
          if [[ $entry != *${ROOTFS_FILE} ]] && [[ $entry != *${SHA256SUM_FILE} ]]; then
            rm -fr $entry
          fi
        done
        break;;
      [Nn]* ) exit;;
      * ) echo "please answer yes or no.";;
    esac
  done
fi

mkdir -p ${LINUX_ROOT}
cd ${LINUX_ROOT}


################################################################################
# fetch and extract ROOTFS
################################################################################

if [ ! -e ${ROOTFS_FILE} ]; then
  wget ${ROOTFS_URL}
fi

if [ ! -e ${SHA256SUM_FILE} ]; then
  wget ${SHA256SUM_URL}
fi

sed -n /${ARCH}/p ${SHA256SUM_FILE} | sha256sum -c || {
  exit
}

echo "extracting ..."
proot --link2symlink tar -xf ${ROOTFS_FILE} --exclude=./dev --exclude=dev


################################################################################
# create startup script
################################################################################

mkdir -p ${HOME}/bin
cat > ${HOME}/bin/${NAME} <<- EOM
getprop | sed -n -e 's/^\[net\.dns.\]: \[\(.*\)\]/\1/p' | sed '/^\s*$/d' | sed 's/^/nameserver /' > ${LINUX_ROOT}/etc/resolv.conf
unset LD_PRELOAD
proot --link2symlink -0 -r ${LINUX_ROOT} -b /dev/ -b /proc/ -b /sdcard -b ${HOME}:/termux -w /sdcard/workdir /usr/bin/env -i HOME=/root TERM="${TERM}" LANG=${LANG} PATH=/usr/local/sbin:/usr/local/bin:/bin:/usr/bin:/sbin:/usr/sbin:/usr/games:/usr/local/games /bin/bash --login
EOM
chmod a+x ${HOME}/bin/${NAME}


################################################################################
# configurations
################################################################################

# mirror
sed -i -e "s/ports\.ubuntu\.com/mirrors\.aliyun\.com/" ${LINUX_ROOT}/etc/apt/sources.list
# vimrc
echo "source /termux/tools/vimrc/_vimrc" > ${LINUX_ROOT}/root/.vimrc

echo
echo "Make sure ~/bin in your PATH, use command ${NAME} to start."

