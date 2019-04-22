#!/bin/bash
if [ -d "~/python" ];then
	Agent_path=~/python
else
	mkdir -p ~/python
	Agent_path=~/python
fi
pip install psutil
sudo mv agent.py ${Agent_path}
