import time

import numpy as np

import tigre
import tigre.algorithms as algs
from tigre.utilities import sl3d
from tigre.utilities import CTnoise
import tigre.utilities.gpu as gpu
import matplotlib.pyplot as plt

rounds = 5
image_sizes = (32, 64, 128, 256, 512, 1024)
dDetector_list = [6.4, 3.2, 1.6, 0.8, 0.4, 0.2]


gpuids = gpu.getGpuIds(gpu.getGpuNames()[0])
print(gpuids)

for idx, image_size in enumerate(image_sizes):
    phatom = sl3d.shepp_logan_3d(size_out=image_size)

    geo = tigre.geometry(mode="cone", default=True, nVoxel=np.array([image_size] * 3))
    dDetector = dDetector_list[idx]
    geo.dDetector = np.array([dDetector, dDetector]) * 2  # size of each pixel            (mm)
    geo.sDetector = geo.dDetector * geo.nDetector

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
