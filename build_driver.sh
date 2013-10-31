#!/bin/bash

CP210X_NAME="cp210x.c"
CP210X_ADDRESS="https://git.kernel.org/cgit/linux/kernel/git/stable/linux-stable.git/plain/drivers/usb/serial/cp210x.c?id=refs/tags/v"

PATCH_NAME="cp210x.patch"

LINUX_KERNEL_VERSION=$(uname -r | cut -f1 -d"-")
LKV_P1=$(echo $LINUX_KERNEL_VERSION | cut -f1 -d".")
LKV_P2=$(echo $LINUX_KERNEL_VERSION | cut -f2 -d".")
LKV_P3=$(echo $LINUX_KERNEL_VERSION | cut -f3 -d".")

if [ $LKV_P3 = 0 ]; then
  CP210X_VERSION=$(echo "$LKV_P1.$LKV_P2")
else
  CP210X_VERSION=$(echo "$LKV_P1.$LKV_P2.$LKV_P3")
fi

#uncomment if patch doesn't work 
#CP210X_VERSION="3.8.0"

#get the file to patch
if [ ! -f $CP210X_NAME ]; then
  wget -O $CP210X_NAME "${CP210X_ADDRESS}${CP210X_VERSION}"
fi

#patch
patch -r - -Np1 < $PATCH_NAME

#run make
make clean
make

echo "
Now to reload the driver type:
  sudo rmmod cp210x
  sudo insmod cp210x.ko
Then try the script:
  ./cp210x_gpio.py [-d /dev/ttyUSB0] [-m 0xf] 0xf
"