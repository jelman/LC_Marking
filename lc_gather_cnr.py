"""
After neuromelanin CNR is calculated and saved to file, this script helps
extract and combine into a single spreadsheet.
"""

import os, sys
import pandas as pd

sys.path.insert(0, '/home/jelman/netshare/K/Projects/LC_Marking/code')
from glob import glob


def cnr_from_file(subjdir, cnrfile):
    """ Extracts contrast values from a given subject in base directory """
    globstr = os.path.join(subjdir, cnrfile)
    lc_cnr_file = glob(globstr)[0]
    subj = os.path.basename(subjdir)
    subj_cnr = pd.read_csv(lc_cnr_file, sep='\t', header=None, index_col=0, names=[subj])
    subj_cnr.index.name = None
    return subj_cnr.T


def get_all_subjs(cnrfile, sublist):
    """ Iterates over all subjects to extract contrast estimates and append to a dataframe """
    all_subjs_cnr = pd.DataFrame()
    for subjdir in sublist:
        subj_cnr = cnr_from_file(subjdir, cnrfile)
        all_subjs_cnr = all_subjs_cnr.append(subj_cnr)
    return all_subjs_cnr


def all_cnr_to_file(outdir, cnrfile, sublist):
    """
    Iterates through specified subject folders and extracts LC CNR estimates.
    Saves to csv in base directory.
    """
    all_subjs_cnr = get_all_subjs(cnrfile, sublist)
    outfile = os.path.join(outdir, os.path.splitext(cnrfile)[0] + '_All.csv')
    all_subjs_cnr.to_csv(outfile, index=True, index_label='vetsaid')


if __name__ == '__main__':

    if len(sys.argv) == 1:
        print 'Combines previously calculated CNR values into a spreadsheet.'
        print 'USAGE: python %s <output directory> <cnr file> <subject dir 1> <subject dir 2> ...' % os.path.basename(sys.argv[0])
        print 'Outputs a csv file with all results to outut directory.'
    else:
        outdir = sys.argv[1]
        cnrfile = sys.argv[2]
        sublist = sys.argv[3:]
        all_cnr_to_file(outdir, cnrfile, sublist)
