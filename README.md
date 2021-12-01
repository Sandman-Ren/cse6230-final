# TIGRE: a MATLAB-GPU toolbox for CBCT image reconstruction

The Tomographic Iterative GPU-based Reconstruction Toolbox (TIGRE) is designed to reduce the gap between image reconstruction research and the end users of tomographic
images. It is an open-source toolbox for fast and accurate 3D tomographic reconstruction for any geometry using higher level abstraction of MATLAB with the lower performance of CUDA. TIGRE focuses on iterative algorithms from a variety of families for improved image quality and leverages the parallel computation capabilities offered by (multiple) GPUs. The goal of the TIGRE toolbox is to provide a fast high-level abstraction of iterative algorithms for image reconstruction in Python and MATLAB while utilizing the performance advantage provided by CUDA.

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

## Benchmarking TIGRE

We benchmarked TIGRE on generated Shepp-Logan Phantoms of varying image sizes using the three methods implemented in TIGRE:
- FDK 
- OS-SART 
- CGLS

There are two evaluation features for our project: 
1. Runtime of the algorithm
2. Normalized root-mean-square deviation(nRMSE). 

With three different methods implemented in TIGRE, the runtime benchmark allow us to find out which method could construct image in the shortest time. Based on the introduction of TIGRE, it is mainly used to reconstruct tomographic images. The current medical industry and applications are looking for a faster reconstruction and scanning which could lead to faster tumours targetting. Additionally, the nRMSE benchmark is a way to test the quality of output image. The normalized RMSE measures the difference between the method output images and the expected result images so that a smaller nRMSE infers a more accurate result. The TIGRE is a medical tool for the medical field so the quality of the image is also essential. A more clear and accurate image could lead to higher accuracy for targetting potential medical issues.

There are four benchmark features that we changed and see how it affects the evaluation result:
1. Number of GPU
2. Image Size
3. Number of Angle
4. Methods

On coc-ice GPU nodes with 1, 2, 3 and 4 GPUs. We provide a Jupyter Notebook where we used Matplotlib to generate graphs
of different configurations versus the averaged running time and the normalized RMSE of each method. Due to the large 
number of configurations we generated, below we pick a few representative examples to demonstrate our benchmarking results.
The full set of graphs can be found under [src/figures/](src/figures/)

## Figure Result Explaination
### Number of GPU
Of our configurations, the number of GPUs on each node is the variable we changed that affected the performance of TIGRE as shown in the Figure 1,2.
We benchmarked different algorithms implemented in TIGRE on nodes with 1, 2, 3 and 4 GPUs. We find that the number of GPUs
reduced the average running time of all the algorithms on larger image sizes. This fits our expectation as parallelizing
the computations on multiple GPUs should speed up the overall computation for all algorithms. On smaller image sizes, having
more GPUs did not have a significant impact on running time. In some such cases, this even resulted in degraded running time.
We believe that this is because the time for data transfer between GPUs and CPU dominated the running time for smaller image
sizes.

### Image Size
From the image 3, we could see that time consumption grows with image size as more data needs to be processed for all three methods. Similarly, the nRMSE grows as image size expands for all three methods as shown in image 4. This may because that it is easier to reconstruct small images than larger images which leads to a smaller nRMSE score for small size. 

### Number of Angle
The figure 5 shows that the runtime increases as the number of angle increases. Based on the figure 6, the nRMSE decreases as the number of angle increases. The trend is the same for all three methods. With increasing number of angles, the algorithm has to handle more projections. Even though this slows down the runtime, the difference between the output and expectation is smaller.

### Methods
In figure 7 and 8, we are comparing how different methods affect the runtime or nRMSE as the image size increase while keep all other variables the same value. Mainly, we want to see how does FDK method different from the other two methods because the OS-SART and CGLS are considered as iterative methods but the FDK is not. From the result, FDK consistently achieves a lower running time and nRMSE score comparing to both of the iterative methods regradless of the image size. This shows that FDK out-perfrom the iterative methods based on our project setting.

## Instructions for running the benchmark computations

To get the benchmark results, first, install TIGRE with the instructions above. Second, login to the coc-ice login node, under [src/benchmark/](src/benchmark/) run the benchmark script. 
```bash
cd src/benchmark/
bash benchmark_job.sh
```
In `benchmark_job.sh`, we submit 8 different jobs separately to have the computation done within the 2-hours wall-time limit. The generated json files are saved under [src/benchmark/](src/benchmark/) as well.

## Benchmark Result

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

