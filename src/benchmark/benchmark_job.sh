# submit each job separately because of the 2 hrs wall time limit
qsub -d $PWD measure_time_GPU_1_nangles_200.pbs
qsub -d $PWD measure_time_GPU_1_nangles_50_100.pbs
qsub -d $PWD measure_time_GPU_2_nangles_200.pbs
qsub -d $PWD measure_time_GPU_2_nangles_50_100.pbs
qsub -d $PWD measure_time_GPU_3_nangles_200.pbs
qsub -d $PWD measure_time_GPU_3_nangles_50_100.pbs
qsub -d $PWD measure_time_GPU_4_nangles_200.pbs
qsub -d $PWD measure_time_GPU_4_nangles_50_100.pbs