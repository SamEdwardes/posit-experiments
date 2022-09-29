---
title: "Using JupyterLab with Conda"
---

## Install

### Install miniconda

Install miniconda:

```bash
curl -O https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh
sudo bash Miniconda3-py39_4.12.0-Linux-x86_64.sh
# when prompted choose to install in /opt/miniconda3
export PATH="/opt/miniconda3/bin:$PATH"
conda init bash
```

Then close and re-open the terminal.

### Install Jupyter

```bash
sudo /opt/miniconda3/condabin/conda install jupyter jupyterlab 
```

### Install R

```bash
export R_VERSION="4.1.2"
curl -O https://cdn.rstudio.com/r/ubuntu-2004/pkgs/r-${R_VERSION}_1_amd64.deb
sudo gdebi -n r-${R_VERSION}_1_amd64.deb
sudo ln -s /opt/R/${R_VERSION}/bin/R /usr/local/bin/R
sudo ln -s /opt/R/${R_VERSION}/bin/Rscript /usr/local/bin/Rscript
```

### Install Workbench

```bash
export RSW_LICENSE="XXXX"
sudo apt-get install -y gdebi-core
curl -O https://download2.rstudio.org/server/bionic/amd64/rstudio-workbench-2022.07.2-576.pro12-amd64.deb
sudo gdebi -n rstudio-workbench-2022.07.2-576.pro12-amd64.deb
sudo rstudio-server license-manager activate $RSW_LICENSE
```

Then create a user for testing:

```bash
sudo useradd --create-home --home-dir /home/sam -s /bin/bash sam;
echo -e 'password\npassword' | sudo passwd sam;
```

Visit the Workbench server and verify that you can login and open RStudio Pro.

```bash
3.139.101.29:8787
```

## Configuration

/etc/rstudio/rserver.conf

```{.ini filename="/etc/rstudio/rserver.conf"}
# Server Configuration File

# Launcher Config
launcher-address=127.0.0.1
launcher-port=5559
launcher-sessions-enabled=1
launcher-default-cluster=Local
launcher-sessions-callback-address=http://127.0.0.1:8787%
```

/etc/rstudio/launcher.conf

```{.ini filename="/etc/rstudio/launcher.conf"}
[server]
address=localhost
port=5559
server-user=rstudio-server
admin-group=rstudio-server
enable-debug-logging=1

[cluster]
name=Local
type=Local
```

etc/rstudio/jupyter.conf

```{.ini filename="/etc/rstudio/jupyter.conf"}
jupyter-exe=/opt/miniconda3/bin/jupyter
notebooks-enabled=1
labs-enabled=1
default-session-cluster=Local
```

Then restart Workbench.

```bash
sudo rstudio-server restart
sudo rstudio-launcher restart
```

Verify that you are able to open a session in JupyterLab and Jupyter Notebook.

## Enable extensions

Install dependencies.

```bash
sudo apt install libcurl4-openssl-dev libssl-dev
```

Download the jupyter lab workbench extension from PyPi <https://pypi.org/project/jupyterlab-workbench/>.

```bash
curl -LO https://pypi.debian.net/pip/pip-18.1.tar.gz
curl -LO https://pypi.debian.net/pip/pip-18.1-py2.py3-none-any.whl
curl -O https://files.pythonhosted.org/packages/92/70/bf70963a3de1e28f82b3c0ee0455a3b54fdab8ba177f183c831c07f039a1/jupyterlab-workbench-0.1.3.tar.gz
curl -O https://files.pythonhosted.org/packages/92/70/bf70963a3de1e28f82b3c0ee0455a3b54fdab8ba177f183c831c07f039a1/jupyterlab-workbench-0.1.3-py2.py3-none-any.whl
sudo /opt/miniconda3/bin/python -m pip install jupyterlab-workbench-0.1.3.tar.gz
```
