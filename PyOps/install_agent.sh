#!/bin/bash
Home_Path=`pwd`
Pack_Path="${Home_Path}/pack"
Python3_Name="Python-3.7.2.tar.xz"
python --version > python_version 2>&1
Python_version=`cat python_version|awk '{print $2}'|awk -F"." '{print $1}'`
if [ -d "~/python" ];then
	Agent_path="~/python"
else
	mkdir -p ~/python
	Agent_path="~/python"
fi
if [ ${Python_version} == 2 ];then
	sudo yum -y install zlib zlib-devel bzip2 bzip2-devel ncurses ncurses-devel readline readline-devel openssl openssl-devel openssl-static xz lzma xz-devel sqlite sqlite-devel gdbm gdbm-devel tk tk-devel libffi libffi-devel
	cd ${Pack_Path} && tar xf ${Python3_Name} && cd Python-* && sudo ./configure --prefix=/usr/local/python --enable-optimizations && sudo make && sudo make install
	cd /usr/bin && sudo ln -s /usr/local/python/bin/* ./
	sudo pip3 install --upgrade pip
	sudo pip3 install psutil
fi
which python3
if [ $? != 0 ];then
	sudo yum -y install zlib zlib-devel bzip2 bzip2-devel ncurses ncurses-devel readline readline-devel openssl openssl-devel openssl-static xz lzma xz-devel sqlite sqlite-devel gdbm gdbm-devel tk tk-devel libffi libffi-devel
	cd ${Pack_Path} && tar xf ${Python3_Name} && cd Python-* && sudo ./configure --prefix=/usr/local/python --enable-optimizations && sudo make && sudo make install
	cd /usr/bin && sudo ln -s /usr/local/python/bin/* ./
	sudo pip3 install --upgrade pip
	sudo pip3 install psutil
fi
cd ${Home_Path} && sudo mv agent.py ${Agent_path}
sudo rm -rf python_version
