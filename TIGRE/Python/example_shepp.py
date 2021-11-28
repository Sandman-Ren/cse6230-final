from __future__ import division
from __future__ import print_function

import numpy as np
import tigre
import tigre.algorithms as algs
from tigre.utilities import sample_loader
from tigre.utilities.Measure_Quality import Measure_Quality
import tigre.utilities.gpu as gpu
import matplotlib.pyplot as plt
from tigre.utilities import sl3d

### This is just a basic example of very few TIGRE functionallity.
# We hihgly recomend checking the Demos folder, where most if not all features of tigre are demoed.


listGpuNames = gpu.getGpuNames()
if len(listGpuNames) == 0:
    print("Error: No gpu found")
else:
    for id in range(len(listGpuNames)):
        print("{}: {}".format(id, listGpuNames[id]))

gpuids = gpu.getGpuIds(listGpuNames[0])
print(gpuids)

## this is Zhenghui's script for using the sl3d.shepp_logan_3d funtion to generate data.
## change nVoxel_size_id to set `nVoxel_dim`  and `dDetector` for different size for the shepp data,
## which are used to set up `geo`

nVoxel_size_id = 1 # from 0 to 4
nVoxel_dim_list = [64, 128, 256, 512, 1024]
dDetector_list = [3.2, 1.6, 0.8, 0.4, 0.2]
nVoxel_dim = nVoxel_dim_list[nVoxel_size_id]
dDetector = dDetector_list[nVoxel_size_id]
nVoxel=np.array([nVoxel_dim, nVoxel_dim, nVoxel_dim])

print('nVoxel_dim',nVoxel_dim)
"""
for shepp 
nVoxel_dim = 128 and geo.dDetector = np.array([1.6, 1.6]) * 2  # size of each pixel     works

"""
# Geometry
geo = tigre.geometry(mode="cone", nVoxel=nVoxel, default=True)
geo.dDetector = np.array([dDetector, dDetector]) * 2  # size of each pixel            (mm)
geo.sDetector = geo.dDetector * geo.nDetector

#%% Define geometry

# phantom_type="kak-slaney"    # Air is 0. Water is 1. Proportional to Hounsfield value.
phantom_type = (
    "yu-ye-wang"  # Default of Python TIGRE Shepp-Logan phantom. Improved visual perception
)
# phantom_type="toft-schabel"  # Default of MATLAB TIGRE Shepp-Logan phantom.
shepp = sl3d.shepp_logan_3d(
    nVoxel_dim, phantom_type=phantom_type
)  # Default are 128^3 and "yu-ye-wang"


nangles = 100
angles = np.linspace(0, 2 * np.pi, nangles, endpoint=False, dtype=np.float32)

# Prepare projection data
print("shepp shape:", shepp.shape)

proj = tigre.Ax(shepp, geo, angles, gpuids=gpuids)

# Reconstruct
niter = 20
fdkout = algs.fdk(proj, geo, angles, gpuids=gpuids)
ossart = algs.ossart(proj, geo, angles, niter, blocksize=20, gpuids=gpuids)

# Measure Quality
# 'RMSE', 'MSSIM', 'SSD', 'UQI'
print("RMSE fdk:")
print(Measure_Quality(fdkout, shepp, ["nRMSE"]))
print("RMSE ossart")
print(Measure_Quality(ossart, shepp, ["nRMSE"]))

# Plot
fig, axes = plt.subplots(3, 2)
axes[0, 0].set_title("FDK")
axes[0, 0].imshow(fdkout[geo.nVoxel[0] // 2])
axes[1, 0].imshow(fdkout[:, geo.nVoxel[1] // 2, :])
axes[2, 0].imshow(fdkout[:, :, geo.nVoxel[2] // 2])
axes[0, 1].set_title("OS-SART")
axes[0, 1].imshow(ossart[geo.nVoxel[0] // 2])
axes[1, 1].imshow(ossart[:, geo.nVoxel[1] // 2, :])
axes[2, 1].imshow(ossart[:, :, geo.nVoxel[2] // 2])
plt.show()
plt.savefig('example_shepp_size_{}.png'.format(nVoxel_dim))
tigre.plotProj(proj)
tigre.plotImg(fdkout)
