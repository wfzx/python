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
def Install_Python() {
    sudo yum -y install zlib zlib-devel bzip2 bzip2-devel ncurses ncurses-devel readline readline-devel openssl openssl-devel openssl-static xz lzma xz-devel sqlite sqlite-devel gdbm gdbm-devel tk tk-devel libffi libffi-devel
	cd ${Pack_Path} && tar xf ${Python3_Name} && cd Python-* && sudo ./configure --prefix=/usr/local/python --enable-optimizations && sudo make && sudo make install
	cd /usr/bin && sudo ln -s /usr/local/python/bin/* ./
	sudo pip3 install --upgrade pip
	sudo pip3 install paramiko
    sudo pip3 install cryptography==2.4.2
	sudo pip3 install psutil
	sftp_client=`sudo find / -name sftp_client.py`
	if [ $? = 0 ];then
	    for i in ${sftp_client}
	    do
            sudo mv ${Home_Path}/sftp_client.py ${i}
        done
    fi
}
if [ ${Python_version} == 2 ];then
	Install_Python
fi
which python3
if [ $? != 0 ];then
	Install_Python
fi
cd ${Home_Path} && sudo mv agent.py ${Agent_path}
sudo rm -rf python_version