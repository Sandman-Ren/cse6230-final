import time

import numpy as np

import tigre
import tigre.algorithms as algs
from tigre.utilities import sl3d
from tigre.utilities import CTnoise
import tigre.utilities.gpu as gpu
import matplotlib.pyplot as plt
from tigre.utilities.Measure_Quality import Measure_Quality

rounds = 5
image_sizes = (32, 64, 128, 256, 512, 1024)
dDetector_list = (6.4, 3.2, 1.6, 0.8, 0.4, 0.2)

niter = 5 

nangles_list = (50, 100)

gpuids = gpu.getGpuIds(gpu.getGpuNames()[0])
print(gpuids)
print(type(gpuids))



num_gpu = len(gpuids)
name_gpu = gpuids.name
measure_file_name = f"data/NumGPU_{num_gpu}_NameGPU_{name_gpu}_NumRound_{rounds}_Data_shepp_nangles_50_100_final.json"


def write_output(method, image_size, nangles, nRMSE, average_time, niter=None,is_last=False):
    with open(measure_file_name, 'a') as fout:
        fout.write('{\n')
        fout.write(f'"method": "{method}",\n')
        fout.write(f'"image_size": {image_size},\n')
        fout.write(f'"nangles": {nangles},\n')
        fout.write(f'"average_time": {average_time},\n')
        if niter:
            fout.write(f'"nRMSE": {nRMSE},\n')
            fout.write(f'"niter": {niter}\n')
        else:
            fout.write(f'"nRMSE": {nRMSE}\n')
        if is_last:
            fout.write("}\n")
        else:      
            fout.write("}\n,\n")

with open(measure_file_name, 'w') as fout:
    fout.write('[\n')
for idx, image_size in enumerate(image_sizes):
    phatom = sl3d.shepp_logan_3d(size_out=image_size)
    for nangles in nangles_list:
        geo = tigre.geometry(mode="cone", default=True, nVoxel=np.array([image_size] * 3))
        dDetector = dDetector_list[idx]
        geo.dDetector = np.array([dDetector, dDetector]) * 2  # size of each pixel            (mm)
        geo.sDetector = geo.dDetector * geo.nDetector

        angles = np.linspace(0, 2 * np.pi, nangles, endpoint=False, dtype=np.float32)

        projections = tigre.Ax(phatom, geo, angles)

        # fdk
        # Warm up
        fdkout = algs.fdk(projections, geo, angles, gpuids=gpuids)

        start_time = time.perf_counter()
        for _ in range(rounds):
            fdkout = algs.fdk(projections, geo, angles, gpuids=gpuids)
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time
        average_time = elapsed_time / rounds
        print(f'method: fdk, image size: {image_size:<4},  average time: {average_time}')
        write_output(method='fdk', image_size=image_size, nangles=nangles, nRMSE=Measure_Quality(fdkout, phatom, ["nRMSE"]),average_time=average_time)
        
        # ossart
        # Warm up
        ossartout = algs.ossart(projections, geo, angles, niter, blocksize=20, gpuids=gpuids)

        start_time = time.perf_counter()
        for _ in range(rounds):
            ossartout = algs.ossart(projections, geo, angles, niter, blocksize=20, gpuids=gpuids)
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time
        average_time = elapsed_time / rounds
        print(f'method: ossart, image size: {image_size:<4},  average time: {average_time}')    

        write_output(method='ossart', image_size=image_size, nangles=nangles, nRMSE=Measure_Quality(ossartout, phatom, ["nRMSE"]),average_time=average_time, niter=niter)

        # CGLS
        # Warm up
        imgCGLS, errL2CGLS = algs.cgls(projections, geo, angles, niter, computel2=True)
        
        start_time = time.perf_counter()
        for _ in range(rounds):
            imgCGLS, errL2CGLS = algs.cgls(projections, geo, angles, niter, computel2=True)
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time
        average_time = elapsed_time / rounds
        print(f'method: CGLS, image size: {image_size:<4},  average time: {average_time}')    
        is_last = False
        if image_size == image_sizes[-1] and nangles==nangles_list[-1]:
            is_last=True
        write_output(method='CGLS', image_size=image_size, nangles=nangles, nRMSE=Measure_Quality(imgCGLS, phatom, ["nRMSE"]),average_time=average_time,niter=niter, is_last=is_last)    

with open(measure_file_name, 'a') as fout:
    fout.write(']\n')