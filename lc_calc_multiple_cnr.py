"""
Takes a list of subjects and calculates neuromelanin CNR for each. These values
are saved out to a file in each subject's directory.
"""

import os, sys
import argparse
import lc_calc_cnr
from glob import glob


def calc_multiple_cnr(basedir, mask_name, sublist, force=False):
    for subj in sublist:
        subjdir = os.path.join(basedir, subj)
        infileglob = os.path.join(subjdir, 'LC_[FT]SE.nii*')
        infile = glob(infileglob)
        if len(infile) > 1:
            raise ValueError('Multiple image files found! %s' % infile)
        else:
            infile = infile[0]
        maskglob = os.path.join(subjdir, mask_name.split(".")[0] + ".nii*")
        mask_file = glob(maskglob)
        if len(mask_file) > 1:
            raise ValueError('Multiple mask files found! %s' % mask_file)
        else:
            mask_file = mask_file[0]
        if os.path.isfile(mask_file):
            lc_calc_cnr.cnr_to_file(infile, mask_file, force=force)
        else:
            continue


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="""This is a  script to calculate LC CNR for multiple subjects and save to file.""")
    parser.add_argument('-d', '--basedir', type=str, required=True,
                        help='Base directory containing subject folders.')
    parser.add_argument('-m', '--mask',required=True, type=str,
                        help='Mask file name. (File containing marked ROIs)')
    parser.add_argument('-s','--subjects', nargs='+', required=True,
                        help='List of subject names')
    parser.add_argument('-f','--force', action="store_true", default=False,
                        help='Force overwrite of existing results file (default = False)')

    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        ### Begin running script ###
        calc_multiple_cnr(args.basedir, args.mask, args.subjects, args.force)
