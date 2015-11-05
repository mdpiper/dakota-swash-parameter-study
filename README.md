# SWASH parameter study with Dakota

A vector parameter study
of the [SWASH](http://swash.sourceforge.net/)
wave-flow model
driven by the 
[Dakota](https://dakota.sandia.gov/)
iterative systems analysis toolkit.

## Description

This study is broken into two stages.

In the first stage,
Dakota,
through the [dakota_run_driver.py](dakota_run_driver.py) script,
creates a series of independent PBS submissions,
one for each iteration of the parameter study (currently 7),
each using the submission script
[run_swash.sh](run_swash.sh).
The submission script uses `mpiexec`
to call SWASH in parallel
using 8 processors
on one compute node.
Output from each run is collected and stored
in `PBS_O_WORKDIR`
in a directory **run.N**,
where N = 1, 2, ..., 7.

In the second stage,
Dakota analyses the results of each iteration
with the [dakota_analysis_driver.py](dakota_analysis_driver.py) script
and creates the tabular output file **dakota.dat**,
which summarizes the results of the parameter study.

## Setup

On ***beach***,
add Dakota paths with:
```
export DAKOTA_DIR=/usr/local/dakota
PATH=$DAKOTA_DIR/bin:$DAKOTA_DIR/test:$PATH
export LD_LIBRARY_PATH=$DAKOTA_DIR/bin:$DAKOTA_DIR/lib:$LD_LIBRARY_PATH
```
Also,
I recommend using the Anaconda Python distribution
instead of the default Python:
```
PATH=/usr/local/anaconda/bin:$PATH
```

## Execution

Run the first stage of the study with:
```
$ dakota -i dakota_run.in -o dakota_run.out &> run.log
```

After the first stage completes, run the second stage with:
```
$ dakota -i dakota_analysis.in -o dakota_analysis.out &> analysis.log
```
