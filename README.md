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

## TODO: Instructions for running the benchmark computations

## Benchmarking TIGRE

We benchmarked TIGRE on generated Shepp-Logan Phantoms of varying image sizes using the three methods implemented in TIGRE:
- FDK
- OS-SART
- CGLS

On coc-ice GPU nodes with 1, 2, 3 and 4 GPUs. We provide a Jupyter Notebook where we used Matplotlib to generate graphs
of different configurations versus the averaged running time and the normalized RMSE of each method. Due to the large 
number of configurations we generated, below we pick a few representative examples to demonstrate our benchmarking results.
The full set of graphs can be found under [src/figures/](src/figures/)

Of our configurations, the number of GPUs on each node is the variable we changed that affected the performance of TIGRE.
We benchmarked different algorithms implemented in TIGRE on nodes with 1, 2, 3 and 4 GPUs. We find that the number of GPUs
reduced the average running time of all the algorithms on larger image sizes. This fits our expectation as parallelizing
the computations on multiple GPUs should speed up the overall computation for all algorithms. On smaller image sizes, having
more GPUs did not have a significant impact on running time. In some such cases, this even resulted in degraded running time.
We believe that this is because the time for data transfer between GPUs and CPU dominated the running time for smaller image
sizes.


![Figure 1: Averaged Runtime of three methods on different number of GPUs
](src/figures/comparison/Number%20of%20angles.200-Image%20Size.1024-Average%20Time.jpg)

*Figure 1: Averaged Runtime of three methods on different number of GPUs*

![Figure 2: Averaged Runtime of three methods on different number of GPUs
](src/figures/comparison/Number%20of%20angles.200-Image%20Size.1024-nRMSE.jpg)

*Figure 2: Normalized RMSE of  the results of the hree methods on different number of GPUs*

![Figure 3: Normalized RMSE of the three methods on different image sizes](src/figures/comparison/Number%20of%20angles.200-Number%20of%20GPUs.4-Average%20Time.jpg)

*Figure 3: Normalized RMSE of the three methods on different image sizes*

![Figure 4: Normalized RMSE of the three methods on different image number of angles](src/figures/comparison/Number%20of%20angles.200-Number%20of%20GPUs.4-nRMSE.jpg)

*Figure 4: Normalized RMSE of the three methods on different image number of angles*

![Figure: Averaged running time of the three methods on different image number of angles](src/figures/comparison/Number%20of%20GPUs.4-Image%20Size.256-Average%20Time.jpg)

*Figure 5: Averaged running time of the three methods on different image number of angles*

![Figure: Normalized RMSE of the three methods on different image number of angles](src/figures/comparison/Number%20of%20GPUs.4-Image%20Size.256-nRMSE.jpg)

*Figure 6: Normalized RMSE of the three methods on different image number of angles*

![Figure: Average running time of the three methods on varying image sizes](src/figures/Number%20of%20angles.100-Number%20of%20GPUs.4-Average%20Time.jpg)

*Figure 7: Average running time of the three methods on varying image sizes*

![Figure: Normalized RMSE of the three methods on varying image sizes, combined](src/figures/Number%20of%20angles.100-Number%20of%20GPUs.4-nRMSE.jpg)

*Figure 8: Averaged running time of the three methods on different image number of angles*