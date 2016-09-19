"""
After neuromelanin CNR is calculated and saved to file, this script helps 
extract and combine into a single spreadsheet.
"""

import os, sys
import pandas as pd

sys.path.insert(0, '/home/jelman/netshare/K/Projects/LC_Marking/code')
from glob import glob


def cnr_from_file(basedir, subj):
    """ Extracts contrast values from a given subject in base directory """
    subjdir = os.path.join(basedir, subj)
    globstr = os.path.join(subjdir, 'LC_CNR.txt')
    lc_cnr_file = glob(globstr)[0]
    subj_cnr = pd.read_csv(lc_cnr_file, sep='\t', header=None, index_col=0, names=[subj])
    subj_cnr.index.name = None
    return subj_cnr.T


def get_all_subjs(basedir, sublist):
    """ Iterates over all subjects to extract contrast estimates and append to a dataframe """
    all_subjs_cnr = pd.DataFrame()
    for subj in sublist:
        subj_cnr = cnr_from_file(basedir, subj)
        all_subjs_cnr = all_subjs_cnr.append(subj_cnr)
    return all_subjs_cnr


def all_cnr_to_file(basedir, sublist):
    """
    Iterates through specified subject folders and extracts LC CNR estimates. 
    Saves to csv in base directory.
    """
    all_subjs_cnr = get_all_subjs(basedir, sublist)
    outfile = os.path.join(basedir, 'AllSubjectsCNR.csv')
    all_subjs_cnr.to_csv(outfile, index=True, index_label='vetsaid')


if __name__ == '__main__':

    if len(sys.argv) == 1:
        print 'Combines previously calculated CNR values into a spreadsheet.'
        print 'USAGE: python %s <base directory name> <subject 1> <subject 2> ...' % os.path.basename(sys.argv[0])
        print 'Outputs a csv file to base directory directory.'
    else:
        basedir = sys.argv[1]
        sublist = sys.argv[2:]
        all_cnr_to_file(basedir, sublist)
