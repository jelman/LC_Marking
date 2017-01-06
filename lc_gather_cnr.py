"""
After neuromelanin CNR is calculated and saved to file, this script helps
extract and combine into a single spreadsheet.
"""

import os, sys
import pandas as pd
import argparse
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
    """
    Extracts contrast values from a given subject in base directory.
    CNR file can be passed with or without file extension.
    """
    cnrfile = os.path.splitext(cnrfile)[0] + '.txt'
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


def all_cnr_to_file(indir, cnrfile, subjects, outfile, method):
    """
    Iterates through specified subject folders and extracts LC CNR estimates.
    Saves to csv in base directory.
    """
    dirlist = [os.path.join(indir, subject) for subject in subjects]
    all_subjs_cnr = get_all_subjs(cnrfile, dirlist, method)
    all_subjs_cnr.to_csv(outfile, index=True, index_label='SubjectID')


if __name__ == '__main__':


    parser = argparse.ArgumentParser(description="""
    This is a  script to calculate LC CNR for multiple subjects and save to file.
    The method to summarise CNR across the three marked slices can be specified.
    """)

    parser.add_argument('indir', type=str,
                        help='Directory containing subject folders')
    parser.add_argument('cnrfile', type=str,
                        help='File name pattern with LC CNR values')
    parser.add_argument('subjects', nargs='+',
                        help='List of subject names')
    parser.add_argument('-o', '--outfile', type=str, required=False,
                    help='Output filename. (default=<indir>/<cnrfile>_All.csv)')
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
        if args.outfile is None:
            outfile = os.path.join(args.indir, os.path.splitext(args.cnrfile)[0]+"_All.csv")
        else:
            outfile = args.outfile
        ### Begin running script ###
        all_cnr_to_file(args.indir, args.cnrfile, args.subjects, outfile, args.method)

# TODO: check to see if script runs...
