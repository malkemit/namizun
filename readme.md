# NAMIZUN

This project is used to remove the limitation of asymmetric ratio for uploading and downloading Iranian servers

## Installation

- 1\) you need to install pip, redis & git:

```bash
sudo apt install python3-pip redis git -y
```
 - 2\) you need to create a directory to clone the project :

```bash
mkdir /var/www/namizun && cd /var/www/namizun
```
- 3\) Clone the project with Git:
```bash
git init
```
```bash
git remote add origin https://github.com/malkemit/namizun.git
```
```bash
git pull origin master
```
- 4\) Install the project requirements with pip:
```bash
pip install -r requirements.txt
```
- 5\) Create service for core.py (for running namizun script):
```bash
sudo nano /etc/systemd/system/namizun.service
```
- 6\) Copy these lines and paste it in the nano editor and save and exit by pressing the **ctrl+o** and **ctrl+x**:
```bash
[Unit]
Description=Namizun service,Asymmetric upload and download

[Service]
Restart=always
ExecStart=/usr/bin/python3 /var/www/namizun/core.py

[Install]
WantedBy=multi-user.target
```
- 7\) Reload the service files to include the new service:
```bash
sudo systemctl daemon-reload
```
- 8\) To enable your service on every reboot:
```bash
sudo systemctl enable namizun.service
```
- 9\) Start namizun service:
```bash
sudo systemctl start namizun.service
```

## Configuration
- You can use **menu.py** tool to configure monitoring. Type the following command to run it:
```bash
python3 /var/www/namizun/menu.py
```
- **Note:** Applying changes until **the end of the uploader cycle does not affect.**\
In fact, after the end of a round of the uploader cycle, the new configurations will have an effect.\
If you want the recorded event to take effect quickly, you can reload the **core.py** with the following command:
```bash
sudo systemctl restart namizun.service
```
## Command list
- 1\) Uploader Running : You can activate or deactivate the uploader by entering the number 1\

- 2\) Speed: By entering the number 2, you can specify the speed of the uploader.(max = 5 normal = 3 min = 1)\
**Note:** that the higher the number, the higher the *CPU consumption* and the sending of *larger buffers*, and the possibility of being *speed limited* by the **provider**.

- 3\) Coefficient: By entering the number 3, you can enter the limit announced by the provider.\
For example, if your ratio should be 10 uploads to 1 download, set the number to 1

  **Important: Your upload and download information will be counted from your last reboot.**\
In fact, as soon as you reboot the server, the amount of downloads and uploads in the program will be zero, and you must manually enter the amount of uploads and downloads you have had so far.

- 4\) Total Upload Before Reboot: By entering the number 4, you can change your upload amount (use the graphs inside the provider panel and enter the correct amount)\

- 5\) Total Download Before Reboot: By entering the number 4, you can change your download amount

- 0\) Exit: goodbye!
## Donate:
 If you enjoyed this script you could donate me by donating!\
Your support allows me to continue my work, **fight against Internet censorship in Iran**

`USDT (TRC20) : TDuBY7FpRkaMU1rhQjQa6sqpNdKhmM8Nx3`\
`Dash : XeCZbBwgoZpZi3RzqkbELvLVTaUCJY67ZL`