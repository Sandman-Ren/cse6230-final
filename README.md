# TIGRE: a MATLAB-GPU toolbox for CBCT image reconstruction

The Tomographic Iterative GPU-based Reconstruction Toolbox (TIGRE) is an open-source toolbox for fast and accurate 3D tomographic reconstruction for any geometry. TIGRE focuses on iterative algorithms from a variety of families for improved image quality and leverages the parallel computation capabilities offered by (multiple) GPUs. The goal of the TIGRE toolbox is to provide a fast high-level abstraction of iterative algorithms for image reconstruction in Python and MATLAB while utilizing the performance advantage provided by CUDA.

## Project Setup

You can find the installation instruction in the official TIGRE repository here: <https://github.com/CERN/TIGRE#installation>

This project is intended to be run on a cluster of GPU nodes. Use the following command to enter into an interactive session on a GPU cluster:

``` shell
qsub -q coc-ice-gpu -l nodes=1:ppn=24:gpus=1 -l walltime=01:00:00 -I
```

Clone the TIGRE repository using the following command:

```shell
git clone https://github.com/CERN/TIGRE.git
```

We will need to install the toolkit on the cluster. This requires several modules:

```shell
module load anaconda3
module load cuda/10.2
```

Install the TIGRE toolkit using the following commands:

```shell
cd TIGRE
cd Python
python3 setup.py install --user
```
