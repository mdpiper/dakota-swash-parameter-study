#! /usr/bin/env bash
# A `qsub` submission script that calls SWASH with `mpiexec`.
#
#PBS -l nodes=1:ppn=8
#PBS -l walltime=12:00:00
#PBS -m abe
#PBS -M mark.piper@colorado.edu

ncpu=`wc -l < $PBS_NODEFILE`
nnodes=`uniq $PBS_NODEFILE | wc -l`
mpiexec=/opt/openmpi/bin/mpiexec
swash=/home/csdms/models/swash/bin/swash-mpi
runcmd="$mpiexec -np $ncpu $swash INPUT"

# Create a working directory on the compute node. Copy the contents of
# the original PBS working directory to it.
working=/state/partition1/$PBS_JOBNAME-$PBS_JOBID
if [ ! -d $working ]; then
    mkdir $working
fi
trap "rm -rf $working" EXIT
cd $working && cp $PBS_O_WORKDIR/* .

echo "--> Running on nodes: " `uniq $PBS_NODEFILE`
echo "--> Number of available cpus: " $ncpu
echo "--> Number of available nodes: " $nnodes
echo "--> Run command: " $runcmd
echo "--> Working directory: " $working
$runcmd

# Copy the completed run back to the original PBS working directory.
cp -R $working/* $PBS_O_WORKDIR
