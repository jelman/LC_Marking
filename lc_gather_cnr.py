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
        top2        :  Average of the top two slices (Default)
        avg         :  Average of all three slices
        max         :  Maximum value from the three slices
        rostral2    :  Average of two most rostral slices
    """
    if method=='top2':
        summ = subj_cnr_all.nlargest(2, 'CNR').mean()
    elif method=='avg':
        summ = subj_cnr_all.mean()
    elif method=='max':
        summ = subj_cnr_all.nlargest(1, 'CNR').mean()
    elif method=='rostral2':
        summ = subj_cnr_all.nsmallest(2, "Slice").mean()
    return summ.drop("Slice")


def cnr_from_file(cnr_file, method):
    """
    Extracts contrast values from a given subject in base directory.
    CNR file can be passed with or without file extension.
    """
    subj_cnr_all = pd.read_csv(cnr_file, sep='\t')
    subj_cnr = summarise_cnr(subj_cnr_all, method)
    return subj_cnr


def get_all_subjs(filelist, method):
    """ Iterates over all files to extract contrast estimates and append to a dataframe """
    all_subjs_cnr = pd.DataFrame()
    for subjfile in filelist:
        subject = os.path.split(os.path.dirname(subjfile))[-1]
        subj_cnr = cnr_from_file(subjfile, method)
        subj_cnr = pd.DataFrame(subj_cnr, columns=[subject]).T
        all_subjs_cnr = all_subjs_cnr.append(subj_cnr)
    return all_subjs_cnr


def all_cnr_to_file(indir, cnrfile, outfile, method):
    """
    Searches through indir for cnrfiles and extracts LC CNR estimates.
    Saves to csv in base directory.
    """
    cnrfile = os.path.splitext(cnrfile)[0] + '.txt'
    globstr = os.path.join(indir, '*/' + cnrfile)
    filelist = glob(globstr)
    all_subjs_cnr = get_all_subjs(filelist, method)
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
    methodgroup.add_argument("--rostral2", action="store_const", dest="method",
                             const="rostral2", help='Average of the 2 most rostral slices')

    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        if args.outfile is None:
            outname = '_'.join([os.path.splitext(args.cnrfile)[0], args.method, "All.csv"])
            outfile = os.path.join(args.indir, outname)
        else:
            outfile = args.outfile
        ### Begin running script ###
        all_cnr_to_file(args.indir, args.cnrfile, outfile, args.method)

# TODO: check to see if script runs...
