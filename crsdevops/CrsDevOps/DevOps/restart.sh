#!/bin/bash
sh pyc.sh
ps -ef|grep "0:9939"|grep -v grep|grep -v $0|awk '{print $2}'|xargs kill -9
nohup python3 manage.py runserver 0:9939 > nohup.out 2>&1 &
python3 manage.py crontab add
