#! /usr/bin/env bash
#
# Calls SWASH with `mpiexec`.
#
#PBS -l nodes=2:ppn=8
#PBS -l walltime=18:00:00
#PBS -m abe
#PBS -M mark.piper@colorado.edu

NCPU=`wc -l < $PBS_NODEFILE`
NNODES=`uniq $PBS_NODEFILE | wc -l`
MPIEXEC=/opt/openmpi/bin/mpiexec
CMD="$MPIEXEC -np $NCPU --verbose"

echo "--> Running on nodes " `uniq $PBS_NODEFILE`
echo "--> Number of available cpus " $NCPU
echo "--> Number of available nodes " $NNODES
echo "--> Launch command is " $CMD

cd $PBS_O_WORKDIR
$CMD swash_mpi.exe INPUT

