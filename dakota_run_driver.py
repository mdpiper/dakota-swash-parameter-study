#! /usr/bin/env python
# Brokers communication between Dakota and SWASH through files.
#
# Arguments:
#   $1 is 'params.in' from Dakota
#   $2 is 'results.out' returned to Dakota

import sys
import os
import shutil
from subprocess import call


def driver():
    """Broker communication between Dakota and SWASH through files."""

    # Files and directories.
    start_dir = os.path.dirname(os.path.realpath(__file__))
    input_file = 'INPUT'
    input_template = input_file + '.template'    
    output_file = 'bot07.mat'
    output_file_var = 'Botlev'
    data_file = 'sand.bot'
    run_script = 'run_swash.sh'

    # Use `dprepro` (from $DAKOTA_DIR/bin) to substitute parameter
    # values from Dakota into the SWASH input template, creating a new
    # SWASH input file.
    shutil.copy(os.path.join(start_dir, input_template), os.curdir)
    call(['dprepro', sys.argv[1], input_template, input_file])

    # Copy the data file into the active directory.
    shutil.copy(os.path.join(start_dir, data_file), os.curdir)

    # Call SWASH through a PBS submission script. Note that `qsub`
    # returns immediately, so jobs do not block.
    job_name = 'SWASH-Dakota' + os.path.splitext(os.getcwd())[-1]
    call(['qsub', '-N', job_name, os.path.join(start_dir, run_script)])

    # Provide a dummy results file to advance Dakota.
    with open(sys.argv[2], 'w') as fp:
        fp.write('0.0\n1.0\n')

if __name__ == '__main__':
    driver()
