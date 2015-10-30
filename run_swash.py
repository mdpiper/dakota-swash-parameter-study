#! /usr/bin/env python
# Brokers communication between Dakota and SWASH through files.
#
# Arguments:
#   $1 is 'params.in' from Dakota
#   $2 is 'results.out' returned to Dakota

import sys
import os
import re
import shutil
from subprocess import call
import numpy as np


def read(output_file, variable=None):
    """Read data from a MATfile. Returns a numpy array, or None on an error."""
    from scipy.io import loadmat
    try:
        mat = loadmat(output_file)
        var = mat[variable]
    except IOError:
        return None
    else:
        return(var)


def write(results_file, array, labels):
    """Write a Dakota results file from an input array."""
    try:
        fp = open(results_file, 'w')
        for i in range(len(array)):
            fp.write(str(array[i]) + '\t' + labels[i] + '\n')
    except IOError:
        raise
    finally:
        fp.close()


def get_labels(params_file):
    """Extract labels from a Dakota parameters file."""
    labels = []
    try:
        fp = open(params_file, 'r')
        for line in fp:
            if re.search('ASV_', line):
                labels.append(''.join(re.findall(':(\S+)', line)))
    except IOError:
        raise
    finally:
        fp.close()
        return(labels)


def main():

    # Files and directories.
    start_dir = os.path.dirname(os.path.realpath(__file__))
    input_template = 'INPUT.template'
    input_file = 'INPUT'
    output_file = 'bot07.mat'
    output_file_var = 'Botlev'

    # Use the parsing utility `dprepro` (from $DAKOTA_DIR/bin) to
    # incorporate the parameters from Dakota into the SWASH input
    # template, creating a new SWASH input file.
    call(['dprepro', sys.argv[1], input_template, input_file])

    # Call SWASH with the new input file.
    call(['swash_mpi.exe', input_file])

    # Calculate the mean and standard deviation of the 'Botlev' output
    # values for the simulation. Write the output to a Dakota results
    # file.
    labels = get_labels(sys.argv[1])
    series = read(output_file, output_file_var)
    if series is not None:
        m_series = [np.mean(series), np.std(series)]
    else:
        m_series = [0, 0]
    write(sys.argv[2], m_series, labels)


if __name__ == '__main__':
    main()
