# NAMIZUN

This project is used to remove the limitation of asymmetric ratio for uploading and downloading Iranian servers

## Installation

**Important Note : use it on ubuntu +20 (python +3.8)**

- 1\) you need to install pip, redis & git:

```bash
sudo apt install python3-pip python3-venv redis git -y
```

- 2\) you need to create a directory to clone the project:

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

- 4\) make virtual environment:

```bash
python3 -m venv /var/www/namizun/venv
```

- 5\) Install the project requirements with pip by **setup.py**:

```bash
source /var/www/namizun/venv/bin/activate && cd /var/www/namizun && pip install . && deactivate
```

- 6\) Create service for uploader.py (for running namizun script):

```bash
ln -s /var/www/namizun/else/namizun.service /etc/systemd/system/
```

**Note:** If you have installed the previous version, you will face the **file exists** error. Remove it with the
following command:

```bash
rm /etc/systemd/system/namizun.service
```

Then enter the command of step 6 (**ln** command)

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

- 10\) Create **namizun** command to execute **menu.py**

```bash
ln -s /var/www/namizun/else/namizun /usr/local/bin/ && chmod +x /usr/local/bin/namizun
```

## Configuration

- You can use **namizun** tool to configure monitoring. Type the following command to run it:

```bash
namizun
```

- **Note:** Applying changes until **the end of the uploader cycle does not affect.**\
  In fact, after the end of a round of the uploader cycle, the new configurations will have an effect.\
  If you want the recorded event to take effect quickly, you can reload the **core.py** with the following command:

```bash
sudo systemctl restart namizun.service
```

## Command list

- this is the menu!

![menu.py](else/menu.png?raw=true)

- 1\) Uploader Running : You can activate or deactivate the uploader by entering the number 1


- 2\) Speed: By entering the number 2, you can specify the speed of the uploader.(max=5 normal=3 min=1)\
  **Note:** that the higher the number, the higher the *CPU consumption* and the sending of *larger buffers*, and the
  possibility of being *speed limited* by the **provider**.


- 3\) Coefficient: By entering the number 3, you can enter the limit announced by the provider.\
  For example, if your ratio should be 10 uploads to 1 download, set the number to 10


  **Important: Your upload and download information will be counted from your last reboot.**\
  In fact, as soon as you reboot the server, the amount of downloads and uploads in the program will be zero, and you
  must manually enter the amount of uploads and downloads you have had so far.


- 4\) Total Upload Before Reboot: By entering the number 4, you can change your upload amount (use the graphs inside the
  provider panel and enter the correct amount)


- 5\) Total Download Before Reboot: By entering the number 5, you can change your download amount


- 0\) Exit: goodbye!

## Notes:
- In this script, you don't need to buy a download host or another server or even upload to your foreign server.\
Only fake traffic will be sent to **Iranian IPs**, which will be lost!


- Although the essence of this script is used to attack, but due to the **limited size of the buffer** and the **distribution of traffic between different IPs**, this does not happen in practice.\
(To attack, many servers must send traffic to one IP, but **this works exactly the opposite**)


- This script is designed to upload up to **50** terabytes of traffic at maximum, it can be used on a server with minimal resources.


- If you want to use a speed of more than 3, be sure to pay attention to the **CPU consumption**.\
High CPU consumption will cause restrictions from the provider (it is better to have at least 2 CPU cores)


- If you are using a **dedicated server**, it is suggested to virtualize it and use your virtual servers.\
In this way, your traffic will be distributed among more IPs and will prevent you from being banned.

## Donate:

If you enjoyed this script you could donate me by donating!\
Your support allows me to continue my work, **fight against Internet censorship in Iran**

`USDT (TRC20) : TDuBY7FpRkaMU1rhQjQa6sqpNdKhmM8Nx3`

`USDT (ERC20) : 0xFAFaf5D1e2e6a11F04e318430ff01031B63A58e1`

`Dash : XeCZbBwgoZpZi3RzqkbELvLVTaUCJY67ZL`