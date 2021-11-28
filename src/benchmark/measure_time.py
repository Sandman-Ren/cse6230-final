import time

import numpy as np

import tigre
import tigre.algorithms as algs
from tigre.utilities import sl3d
from tigre.utilities import CTnoise
import tigre.utilities.gpu as gpu


rounds = 5
image_sizes = (32, 64, 128, 256, 512, 1024)

gpuids = gpu.getGpuIds(gpu.getGpuNames()[0])
print(gpuids)

for image_size in image_sizes:
    phatom = sl3d.shepp_logan_3d(size_out=image_size)

    geo = tigre.geometry(mode="cone", default=True, nVoxel=np.array([image_size] * 3))
    angles = np.linspace(0, 2 * np.pi, 100)
    projections = tigre.Ax(phatom, geo, angles)

    # Warm up
    fdkout = algs.fdk(projections, geo, angles, gpuids=gpuids)

    start_time = time.perf_counter()
    for _ in range(rounds):
        fdkout = algs.fdk(projections, geo, angles, gpuids=gpuids)
    end_time = time.perf_counter()

    elapsed_time = end_time - start_time
    average_time = elapsed_time / rounds
    print(f'image size: {image_size:<4}  average time: {average_time}')
