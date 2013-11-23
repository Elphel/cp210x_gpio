#!/usr/bin/python
#-----------------------------------------------------------------------------
# FILE NAME  : cp210x_gpio.py
# DESCRIPTION: control GPIO pins for CP210X USB to UART Bridges
# Copyright (C) 2013 Elphel, Inc
#-----------------------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# The four essential freedoms with GNU GPL software are:
# * to run the program for any purpose
# * to study how the program works and change it to make it do what you wish
# * to redistribute copies so you can help your neighbor
# * to distribute copies of your modified versions to others
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-----------------------------------------------------------------------------
__author__ = "Oleg Dzhimiev"
__copyright__ = "Copyright 2013, Elphel, Inc."
__license__ = "GPL"
__version__ = "3.0+"
__maintainer__ = "Oleg Dzhimiev"
__email__ = "oleg@elphel.com"
__status__ = "Released"

import array, fcntl, os, errno
import argparse # http://docs.python.org/2/howto/argparse.html

IOCTL_GPIOGET = 0x8000
IOCTL_GPIOSET = 0x8001

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--device', default="/dev/ttyUSB0", help='USB device. Default: /dev/ttyUSB0')
parser.add_argument("gpio_value", default=None, nargs='?', help="hex value for GPIO. Example (GPIO[3:0]): 0xf - all 1's, 0x0 - all 0's. If not specified - read GPIO only")
parser.add_argument('-m', '--mask', default="0xff",help='hex value for masking out GPIO bits: 1 - enable rewrite, 0 - disable. Example (GPIO[3:0]): -m 0xf')
args = parser.parse_args()
device=args.device
if args.gpio_value is None:
    mask = 0x00
    gpio = (0xff<<16)|mask

else:    
    mask = int(args.mask,0)
    gpio = (int(args.gpio_value,0)<<16)|mask

print ('Target GPIO value: 0x%x, mask: 0x%x'%(gpio,mask))

try:
    fd = open(device, 'r+')
except IOError, ioex:
    if (errno.errorcode[ioex.errno]=='EACCES'):
        print "\nDid you forget to use 'sudo' ?\n"
    raise Exception(str(device)+' - '+os.strerror(ioex.errno))

buf = array.array('l', [0])
fcntl.ioctl(fd, IOCTL_GPIOGET, buf, 1)
print ('Old GPIO value:'),hex(buf[0])

if args.gpio_value is None:
  exit (0)
  
buf[0] = gpio
fcntl.ioctl(fd, IOCTL_GPIOSET, buf, 1)
fcntl.ioctl(fd, IOCTL_GPIOGET, buf, 1)
print ('New GPIO value:'),hex(buf[0])

