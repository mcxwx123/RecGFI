## Hardware environment 

We conduct development and execute all our experiments on a Ubuntu 20.04 server with two Intel Xeon Gold CPUs, 320GB memory, and 36TB RAID 5 Storage. We have also vetted this replication package in a Ubuntu 20.04 VirtualBox VM with 1 CPU Core, 8GB Memory and 100GB storage, and a Windows 10 machine with 8 CPU Cores and 8GB Memory.

## Software environment

The software requirements for this replication package has already been described in the README and the requirements-lock.txt file in this folder. We recommend to either exactly follow the installation commands to configure an Anaconda environment as follows, or to directly use the VM Image. Although we have only tested our replication package on Ubuntu 20.04 and Windows 10, it should also work in other common OS because we do not rely on any OS specific features.

```shell script
conda create -n RecGFI python=3.8
conda activate RecGFI
python -m pip install -r requirements-lock.txt
```

The VM image for this artifact is available at Zenodo.
