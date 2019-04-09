#!/usr/bin/python3

import psutil

#内存使用率
print ("Mem:%.f%%" % (psutil.virtual_memory().percent))

#cpu使用率
print ("CPU:%.f%%" % (psutil.cpu_percent(1)))

#磁盘使用率
print ("Disk:%.f%%" % (psutil.disk_usage("/").percent))

