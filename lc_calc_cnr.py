"""
This script calculates neuromelanin contrast to noise ratio and saves to file.
The CNR is calculated (LC - PT) / PT, where LC is the average signal of left
and right LC, and PT is the pontine tegmentum. Individual ROI values, averaged
LC ROI value, and CNR value are saved to a text file.
"""

import argparse
import os, sys
import nibabel as nib
import logging
import numpy as np
import pandas as pd
from utils.create_logger import create_logger
from utils.lc_error_checks import run_error_checks


def make_outfile(root, name='LC_CNR.txt'):
    """ generate outfile string
    check if files exists
    return exists, file_string
    """
    outfile = os.path.join(root, name)
    exists = False
    if os.path.isfile(outfile):
        exists = True
    return exists, outfile


def get_roi_vals(infile, mask_file):
    """
    Gets average value within each ROI. Takes LC FSE image and mask file
    containing ROIs of left LC (label=1), right LC (label=2), and
    pontine tegmentum (label=3). Loops over slices to get separate values
    for each slice and saves to dataframe.
    """
    # Load files
    img = nib.load(infile)
    img_data = img.get_fdata()
    mask = nib.load(mask_file)
    mask_data = mask.get_fdata()
    slices = np.unique(np.where(mask_data != 0)[2])
    colnames = ['Left_LC','Right_LC','PT']
    # Initialize dataframe to hold results
    resultsdf = pd.DataFrame(index=slices, columns=colnames)
    for slicenum in slices:
        resultsdf.loc[slicenum,:] = get_slice_vals(img_data[:,:,slicenum], mask_data[:,:,slicenum])
    return resultsdf


def get_slice_vals(slice_data, slice_mask):
    """
    Takes data from one slice and gets values for each ROI. ROIs should be
    left LC (label=1), right LC (label=2), and pontine tegmentum (label=3).
    """
    # Extract mean values from each ROI
    lLC_mean = slice_data[slice_mask == 1].mean()
    rLC_mean = slice_data[slice_mask == 2].mean()
    PT_mean = slice_data[slice_mask == 3].mean()
    return [lLC_mean, rLC_mean, PT_mean]


def get_cnr(lLC_mean, rLC_mean, PT_mean):
    """Calculate contrast ratio of locus coeruleus to pontine tegmentum"""
    LC_mean = (lLC_mean + rLC_mean) / 2
    mean_cnr = (LC_mean - PT_mean) / PT_mean
    left_cnr = (lLC_mean - PT_mean) / PT_mean
    right_cnr = (rLC_mean - PT_mean) / PT_mean
    return pd.concat([mean_cnr, left_cnr, right_cnr], axis=1)


def cnr_to_file(infile, mask_file, outdir=None, force=False):
    if outdir == None:
        outdir, _ = os.path.split(infile)
    # Name outfile based on mask file
    fname = os.path.basename(mask_file).split('.')[0] + '.txt'
    exists, outfile = make_outfile(outdir, fname)
    if (exists and force == False):
        print("{} exists, delete before running or use --force flag.".format(outfile))
        return
    # Create logger
    logname = 'calc_cnr_' + os.path.basename(mask_file).split('.')[0] + '.log'
    logger = create_logger(outdir, name=logname)
    logger.info("Image file: {}".format(infile))
    logger.info("Mask file: {}".format(mask_file))
    # Run error checks
    error_status = run_error_checks(mask_file)
    # Get ROI values put into dataframe
    resultsdf = get_roi_vals(infile, mask_file)
    # Change slices from 0-based index to 1-based
    resultsdf.index = resultsdf.index + 1
    # Calculate contrast to noise ratio
    resultsdf[['CNR', 'Left_CNR', 'Right_CNR']] = get_cnr(resultsdf['Left_LC'], resultsdf['Right_LC'], resultsdf['PT'])
    # Save results to file
    try:
        resultsdf.to_csv(outfile, index_label="Slice", sep="\t")
    except IOError:
        print('File could not be saved')
    logger.info("Results saved to: {}".format(outfile))
    # Close log files
    for hndlr in logger.handlers[:]:
        logger.removeHandler(hndlr)
        hndlr.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""This is a  script to calculate LC CNR for a single subject and save to file.""")
    parser.add_argument('-i', '--infile', type=str, required=True,
                        help='LC FSE file name.')
    parser.add_argument('-m', '--mask', required=True, type=str,
                        help='Mask file name. (File containing marked ROIs)')
    parser.add_argument('-o', '--outdir', required=False,
                        help='Output directory name. (default = input file directory)')
    parser.add_argument('-f', '--force', action="store_true", default=False,
                        help='Force overwrite of existing results file (default = False)')

    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        if args.outdir is None:
            args.outdir, _ = os.path.split(args.infile)
        ### Begin running script ###
        cnr_to_file(args.infile, args.mask, args.outdir, args.force)

### TODO: Adapt function to extract ROI values to three slices
