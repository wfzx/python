#!/usr/bin/env python

import psutil

#Mem
print ("Mem:%.f%%" % (psutil.virtual_memory().percent))

#cpu
print ("CPU:%.f%%" % (psutil.cpu_percent(1)))

#Disk
print ("Disk:%.f%%" % (psutil.disk_usage("/").percent))

