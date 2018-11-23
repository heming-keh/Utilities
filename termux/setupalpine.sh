# bash setupalpine.sh
# requirements: wget tar proot


VERSION="3.8"
MINOR_VERSION="1"
# getprop ro.product.cpu.abi
ARCH="aarch64"

MINROOTFS_URL="https://mirrors.aliyun.com/alpine/v${VERSION}/releases/${ARCH}/alpine-minirootfs-${VERSION}.${MINOR_VERSION}-${ARCH}.tar.gz"
MINROOTFS_FILE=${MINROOTFS_URL##*/}
ALPINE_ROOT="${HOME}/alpine"


# create ${ALPINE_ROOT}
if [ -d ${ALPINE_ROOT} ]; then
  while true; do
    read -p "apline already exists, do you want to delete it? " yn
    case ${yn} in
      [Yy]* )
        for entry in ${ALPINE_ROOT}/*; do
          if [[ $entry != *${MINROOTFS_FILE} ]]; then
            rm -fr $entry
          fi
        done
        break;;
      [Nn]* ) exit;;
      * ) echo "please answer yes or no.";;
    esac
  done
fi

mkdir -p ${ALPINE_ROOT}
cd ${ALPINE_ROOT}


# fetch and extract ROOTFS
if [ ! -e ${MINROOTFS_FILE} ]; then
  wget ${MINROOTFS_URL}
  wget ${MINROOTFS_URL}.sha256
  sha256sum -c ${MINROOTFS_FILE}.sha256 || {
    exit
  }
fi
proot --link2symlink tar -xf ${MINROOTFS_FILE} --exclude=./dev


# create alpine startup script
mkdir -p ${HOME}/bin
cat > ${HOME}/bin/alpine <<- EOM
ALPINE_ROOT="${HOME}/alpine"
getprop | sed -n -e 's/^\[net\.dns.\]: \[\(.*\)\]/\1/p' | sed '/^\s*$/d' | sed 's/^/nameserver /' > ${ALPINE_ROOT}/etc/resolv.conf
unset LD_PRELOAD
proot --link2symlink -0 -r ${ALPINE_ROOT} -b /dev/ -b /proc/ -b /sdcard -b ${HOME}:/root -w /root /usr/bin/env HOME=/root TERM="${TERM}" LANG=${LANG} PATH=/bin:/usr/bin:/sbin:/usr/sbin /bin/sh --login
EOM
chmod a+x ${HOME}/bin/alpine


# repositories
sed -i -e "s/^/#/" ${ALPINE_ROOT}/etc/apk/repositories
echo "http://mirrors.aliyun.com/alpine/${VERSION}/main" >> ${ALPINE_ROOT}/etc/apk/repositories
echo "http://mirrors.aliyun.com/alpine/${VERSION}/community" >> ${ALPINE_ROOT}/etc/apk/repositories


echo "done"
