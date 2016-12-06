"""
After neuromelanin CNR is calculated and saved to file, this script helps
extract and combine into a single spreadsheet.
"""

import os, sys
import pandas as pd
import argparse
sys.path.insert(0, '/home/jelman/netshare/K/Projects/LC_Marking/code')
from glob import glob


def summarise_cnr(subj_cnr_all, method='top2'):
    """ 
    Summarize CNR for a subject.
    Methods
    --------------
        top2 :  Average of the top two slices (Default)
        avg  :  Average of all three slices 
        max  :  Maximum value from the three slices
    """
    if method=='top2':
        summ = subj_cnr_all.nlargest(2, 'CNR').mean()
    elif method=='avg':
        summ = subj_cnr_all.mean()
    elif method=='max':
        summ = subj_cnr_all.nlargest(1, 'CNR').mean()
    return summ.drop("Slice")       

def cnr_from_file(subjdir, cnrfile, method):
    """ Extracts contrast values from a given subject in base directory """
    globstr = os.path.join(subjdir, cnrfile)
    lc_cnr_file = glob(globstr)[0]
    subj_cnr_all = pd.read_csv(lc_cnr_file, sep='\t')
    subj_cnr = summarise_cnr(subj_cnr_all, method)
    return subj_cnr


def get_all_subjs(cnrfile, dirlist, method):
    """ Iterates over all subjects to extract contrast estimates and append to a dataframe """
    all_subjs_cnr = pd.DataFrame()
    for subjdir in dirlist:
        subject = os.path.basename(subjdir)
        subj_cnr = cnr_from_file(subjdir, cnrfile, method)
        subj_cnr = pd.DataFrame(subj_cnr, columns=[subject]).T
        all_subjs_cnr = all_subjs_cnr.append(subj_cnr)
    return all_subjs_cnr


def all_cnr_to_file(outdir, cnrfile, dirlist, method):
    """
    Iterates through specified subject folders and extracts LC CNR estimates.
    Saves to csv in base directory.
    """
    all_subjs_cnr = get_all_subjs(cnrfile, dirlist, method)
    outfile = os.path.join(outdir, os.path.splitext(cnrfile)[0] + '_All.csv')
    all_subjs_cnr.to_csv(outfile, index=True, index_label='SubjectID')


if __name__ == '__main__':


    parser = argparse.ArgumentParser(description="""
    This is a  script to calculate LC CNR for multiple subjects and save to file. 
    The method to summarise CNR across the three marked slices can be specified.
    """)
    parser.add_argument('outdir', type=str,  
                        help='Directory to save files to.')
    parser.add_argument('cnrfile', type=str, 
                        help='File name pattern with LC CNR values')
    parser.add_argument('subdirs', nargs='+',  
                        help='List of subject directories')
    methodgroup = parser.add_mutually_exclusive_group()
    methodgroup.add_argument("--top2", action="store_const", dest="method", 
                             const="top2", default="top2",
                             help='Average of top 2 CNR values (default)')
    methodgroup.add_argument("--avg", action="store_const", dest="method", 
                             const="avg", help='Average of all CNR values')
    methodgroup.add_argument("--max", action="store_const", dest="method", 
                             const="max", help='Maxmimum CNR value only')

  
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        ### Begin running script ###
        all_cnr_to_file(args.outdir, args.cnrfile, args.subdirs, args.method)

# TODO: check to see if script runs...