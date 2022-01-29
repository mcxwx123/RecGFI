## Replication Package Setup

In this section, we introduce how to set up the required environment for the reproducible results in the paper. First, clone this repository or download the repository archive from Zenodo.

Switch to the `RecGFI` folder. We use Anaconda for Python development. Configure a new Conda environment by executing the following commands:

```shell script
conda create -n RecGFI python=3.8
conda activate RecGFI
python -m pip install -r requirements-lock.txt
```

If you download repository archive from Zenodo, you can already find the issue dataset at `RecGFI/data/issuedata.json`.  However, it is too large (1.6GB) for git, so if you clone from GitHub, please download this file separately from Zenodo and put it there.

### Using the VirtualBox VM Image

To ease the burden to build the required environment, we supply a VirtualBox VM Image to replicate experimental results quickly and easily. You can download the VM Image from Zenodo. Then register and open it with VirtualBox VM. The password is icse22ae. You can see a folder named `RecGFI` in the Desktop with everything already configured.