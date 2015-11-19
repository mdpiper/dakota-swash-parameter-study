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


def read(output_file, variable=None):
    """Read data from a MATfile. Return a numpy array."""
    from scipy.io import loadmat
    try:
        mat = loadmat(output_file)
        var = mat[variable]
    except:
        raise
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


def driver():
    """Broker communication between Dakota and SWASH through files."""

    # Files and directories.
    start_dir = os.path.dirname(os.path.realpath(__file__))
    output_file = 'ufric07.mat'
    output_var = 'Ufric_x_002800_000' # final time step

    # Calculate the mean and standard deviation of the 'Botlev' output
    # values for the simulation. Write the output to a Dakota results
    # file.
    labels = get_labels(sys.argv[1])
    output = read(output_file, output_var)
    if output is not None:
        m_output = [output.mean(), output.std()]
    else:
        m_output = [0, 0]
    write(sys.argv[2], m_output, labels)


if __name__ == '__main__':
    driver()
