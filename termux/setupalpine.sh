# bash setupalpine.sh
# requirements: wget tar proot


################################################################################
# settings
################################################################################

VERSION="3.8"
VERSION_MINOR="1"
# getprop ro.product.cpu.abi
ARCH="aarch64"
NAME="alpine"

ROOTFS_URL="https://mirrors.aliyun.com/alpine/v${VERSION}/releases/${ARCH}/alpine-minirootfs-${VERSION}.${VERSION_MINOR}-${ARCH}.tar.gz"
SHA256SUM_URL="${ROOTFS_URL}.sha256"
ROOTFS_FILE=${ROOTFS_URL##*/}
SHA256SUM_FILE=${SHA256SUM_URL##*/}
LINUX_ROOT="${HOME}/.${NAME}"


################################################################################
# create ${LINUX_ROOT}
################################################################################

if [ -d ${LINUX_ROOT} ]; then
  while true; do
    read -p "apline already exists, do you want to delete it? " yn
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

sha256sum -c ${SHA256SUM_FILE} || {
  exit
}

echo "extracting ..."
proot --link2symlink tar -xf ${ROOTFS_FILE} --exclude=./dev


################################################################################
# create alpine startup script
################################################################################

mkdir -p ${HOME}/bin
cat > ${HOME}/bin/${NAME} <<- EOM
getprop | sed -n -e 's/^\[net\.dns.\]: \[\(.*\)\]/\1/p' | sed '/^\s*$/d' | sed 's/^/nameserver /' > ${LINUX_ROOT}/etc/resolv.conf
unset LD_PRELOAD
proot --link2symlink -0 -r ${LINUX_ROOT} -b /dev/ -b /proc/ -b /sdcard -b ${HOME}:/root -w /root /usr/bin/env HOME=/root TERM="${TERM}" LANG=${LANG} PATH=/bin:/usr/bin:/sbin:/usr/sbin /bin/sh --login
EOM
chmod a+x ${HOME}/bin/${NAME}


################################################################################
# repositories
################################################################################

sed -i -e "s/^/#/" ${LINUX_ROOT}/etc/apk/repositories
echo "http://mirrors.aliyun.com/alpine/v${VERSION}/main" >> ${LINUX_ROOT}/etc/apk/repositories
echo "http://mirrors.aliyun.com/alpine/v${VERSION}/community" >> ${LINUX_ROOT}/etc/apk/repositories


echo
echo "Make sure ~/bin in your PATH, use command ${NAME} to start."

