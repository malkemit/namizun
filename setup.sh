#!/usr/bin/env bash

echo 'installing prerequests'
apt update && apt install python3-pip python3-venv redis git -y
if [ $? == 0 ]
then
	echo 'installing done'
else
	echo 'something went wrong with installing'
	exit
fi


echo 'start redis service'
systemctl start redis.service
if [ $? == 0 ]
then
	echo 'redis servie started'
else
	echo 'service starting failed'
	exit
fi


echo 'pulling the repostory'
git clone https://github.com/offline-pirate/namizun.git /var/www/namizun
if [ $? != 0 ]
then
	echo 'could not clone the repository'
	exit
fi


echo 'create virtual env'
python3 -m venv /var/www/namizun/venv
if [ $? != 0 ]
then
	echo 'venv didnt created'
fi


echo 'installing project dependencies'
cd /var/www/namizun && source /var/www/namizun/venv/bin/activate && pip install wheel && pip install namizun_core/ namizun_menu/ && deactivate
if [ $? != 0 ]
then
	echo 'depencensies doesnt installed correctlly'
	exit
fi

echo 'create service'
ln -s /var/www/namizun/else/namizun.service /etc/systemd/system/
if [ $? != 0 ]
then
	echo 'creating service was failed'
	exit
fi

## starging the services
systemctl daemon-reload


echo 'starting namizun service'
sudo systemctl enable namizun.service
sudo systemctl start namizun.service
if [ $? != 0 ]
then
	echo 'service namizun didnt started'
	exit
fi


echo 'make namizun as a command'
ln -s /var/www/namizun/else/namizun /usr/local/bin/ && chmod +x /usr/local/bin/namizun
if [ $? != 0 ]
then
	echo 'failed to add namizun to PATH environment variables'
	exit
fi

