# CP210x GPIO control
A patch to the CP210x USB to UART Bridges driver that adds GPIO pins control by implementing ioctl function and a python script to program devices.

## Supported OS
* Kubuntu Linux 13.04 (kernel 3.8.0-32)

## Tested devices
* CP2103
* CP2104

## Install
1. Build:

        ./build_driver

2. Reload driver (from the built directory):

        sudo rmmod cp210x
        sudo insmod cp210x.ko

## Program GPIO_MAS
1. Examples:
    * Set all 1's:

            sudo ./cp210x_gpio.py -d /dev/ttyUSB0 -m 0xff 0xff

    * Set GPIO[3]=1, others - 0:
    
            sudo ./cp210x_gpio.py -d /dev/ttyUSB1 -m 0xff 0x08
    
## Changes in the driver
* Changes in the driver cp210x.c are based on the patch found [here](https://lkml.org/lkml/2012/5/1/2)
* GPIO_VALUE=arg[23:16], GPIO_MASK=arg[7:0]

## Unresolved questions
* Silabs drivers in 2.6.x and 3.x.x for GPIOs differ: 
    * 2.6.x: GPIO_VALUE=arg[23:16], GPIO_MASK=arg[7:0] - this matches the patch
    * 3.x.x: GPIO_VALUE=arg[15: 8], GPIO_MASK=arg[7:0]

## Links
* [Silabs CP210x USB to UART Bridge VCP Drivers](http://www.silabs.com/products/mcu/pages/usbtouartbridgevcpdrivers.aspx) - supported kernels 2.6.x, 3.x.x (but 3.x.x are not up-to-date - cannot be built in 3.8.0)
* [cp210x: Add ioctl for GPIO support](https://lkml.org/lkml/2012/5/1/2) - patch