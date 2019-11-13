#!/bin/bash
ps -ef|grep python|grep -v grep|grep -v $0|awk '{print $2}'|xargs kill -9 



nohup python3 manage.py runserver &
