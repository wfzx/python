#!/bin/bash

find ./ -name __pycache__ |xargs rm -rf
pynum=`find ./ -name "*.py">py.txt`
find ./ -name "*.py"|xargs python3 -m py_compile
for i in `cat py.txt`
do
	if [ ${i} == "./manage.py" ];then
		continue
	fi
	pyname=`echo ${i}|awk -F'/' '{print $NF}'`
	dir=`echo ${i}|awk -F${pyname} '{print $1}'`
	name=`echo ${pyname}|awk -F'.' '{print $1}'`
	pycdir=`find ${dir}__pycache__ -name "${name}*.pyc"`
	echo "pyname:${pyname}"
	echo "dir:${dir}"
	echo "name:${name}"
	echo "pycdir:${pycdir}"
	echo "exec: mv ${pycdir} ${dir}${name}.pyc"
	echo "exec: rm -rf ${dir}${name}.py"
	mv ${pycdir} ${dir}${name}.pyc
	rm -rf ${dir}${name}.py
	echo ""
	echo ""
	echo ""
	echo ""
	echo ""
	echo ""
	echo ""
	echo ""
	echo ""
	echo ""
	echo ""
done
find ./ -name __pycache__|xargs rm -rf
