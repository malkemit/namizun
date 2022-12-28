#!/usr/bin/env bash

echo 'Install prerequisites (step 1)'
apt update && apt install python3-pip python3-venv redis git -y
if [ $? == 0 ]; then
  echo 'Successfully installed'
else
  echo 'An error occurred while installing the prerequisites'
  exit
fi

echo 'start redis service'
systemctl start redis.service
if [ $? == 0 ]; then
  echo 'redis servie started'
else
  echo 'service starting failed'
  exit
fi

echo "Creating namizun directory (step 2)"
mkdir -p /var/www/namizun && cd /var/www/namizun

echo 'Pulling the repository (step 3)'
git init
git remote add origin https://github.com/malkemit/namizun.git
git pull origin master
if [ $? != 0 ]; then
  echo 'could not clone the repository'
  exit
fi

echo 'Create virtual env (step 4)'
python3 -m venv /var/www/namizun/venv
if [ $? != 0 ]; then
  echo "VENV didn't created"
fi

echo 'Installing project dependencies (step 5)'
cd /var/www/namizun && source /var/www/namizun/venv/bin/activate && pip install wheel && pip install namizun_core/ namizun_menu/ && deactivate
if [ $? != 0 ]; then
  echo "Dependencies doesn't installed correctly"
  exit
fi

echo 'Create namizun service (step 6)'
ln -s /var/www/namizun/else/namizun.service /etc/systemd/system/
if [ $? != 0 ]; then
  echo 'Creating service was failed'
  exit
fi

echo 'Reload services and start namizun.service (step 7)'
systemctl daemon-reload
sudo systemctl enable namizun.service
sudo systemctl start namizun.service
if [ $? != 0 ]; then
  echo "Namizun service didn't started"
  exit
fi

echo "make namizun as a command (step 8)"
ln -s /var/www/namizun/else/namizun /usr/local/bin/ && chmod +x /usr/local/bin/namizun
if [ $? != 0 ]; then
  echo "failed to add namizun to PATH environment variables"
  exit
fi