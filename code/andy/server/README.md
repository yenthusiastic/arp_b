# Server

## Quick guide
### Install Pyota
```bash
sudo adduser hubuser
source hubenv/bin/activate
pip3 install pyota[ccurl]
```


## Complete documentation starting from openresty-snapshot
Install Python3.7 and set as standard for *python* and *python3*.

Install NPM and NodeJS.

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7 python3.7-venv python3.7-dev
sudo apt purge python2.7-minimal
sudo apt purge python2.7
sudo apt autoremove
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
sudo update-alternatives  --set python /usr/bin/python3.7
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1
sudo update-alternatives  --set python3 /usr/bin/python3.7
sudo apt install python-apt
sudo apt install software-properties-common
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py --force-reinstall
sudo python3 get-pip.py --force-reinstall
pip3 install --upgrade pip
sudo apt install npm nodejs-legacy
sudo npm install -g configurable-http-proxy

```


Make virtual environment and install JupyterHub.

```bash
sudo adduser hubuser
sudo su hubuser
cd
python3.7 -m venv hubenv
source hubenv/bin/activate
pip3 install jupyterhub
pip3 install --upgrade notebook
```


## Execute JupyterHub
Execute in terminal:
`sudo /bin/sh /home/hubuser/lauch.sh`

Execute in screen session at startup:

`@reboot /bin/bash && screen -dmS jupyterhub && screen -S jupyterhub -p 0 -X stuff "sudo -S -i /bin/sh /home/hubuser/lauch.sh^M" &`


### [Sharing Data](http://tljh.jupyter.org/en/latest/howto/content/share-data.html)
```bash
sudo mkdir -p /srv/data/shared_data
sudo chmod 777 /srv/data/shared_data
```

In every user's *notebooks* directory:
```bash
sudo ln -s /srv/data/shared_data shared_data
sudo chown <USERNAME> shared_data
```

### Install package for all users (python3 kernel)
Login as user hubuser, open venv, install package.
```bash
source hubenv/bin/activate
pip install pyqrcode
```

### pyota
```bash
sudo apt install python3.6 python3.6-venv python3.6-dev
sudo su hubuser
cd /home/hubuser
python3.6 -m venv pyota_env
source pyota_env
python -m ipykernel install --user --name pyota --display-name "pyota_3.6"
```

### Custom Kernel
Go to home directory, make a virtual environment (here: *NAME_venv*) and open it:
```bash
cd
python3.7 -m venv NAME_env
source NAME_env/bin/activate
```
Install custom packages, for example numpy:
`pip install --user numpy`

Create kernel from your venv just for your user, also add your user name to it (here: *my_kernel_USER*):
 - name: name inside jupyter
 - display-name: name displayed inside notebook in kernel selection

`python -m ipykernel install --user --name mykernel_USER  --display-name "mykernel_USER"`

Stop all your notebook servers for the changes to take effect.
You can now select the kernel inside a notebook.
If you install more packages afterwards, the above command has to be excecuted again, to override the old kernel version.


### Make Group 'jupyterhub' and add users
> GroupID need to be unique (here 10000)
```bash
sudo groupadd -g 10000 jupyterhub
sudo adduser test jupyterhub
```


## Run JupyterHub without sudo
[Source](https://jupyterhub.readthedocs.io/en/stable/reference/config-sudo.html)

Make new user

`sudo adduser hubuser`

Add to group
