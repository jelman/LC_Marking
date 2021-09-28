"""
After neuromelanin CNR is calculated and saved to file, this script helps
extract and combine into a single spreadsheet.
"""

import os, sys
import pandas as pd
import argparse
from glob import glob


def summarise_cnr(subj_cnr_all):
    """
    Summarize CNR for a subject.
    Methods
    --------------
        rostral2    :  Average of two most rostral slices 
        avg3         :  Average of all three slices
        max1         :  Maximum value from the three slices
        rostral1    :  Value of the single most rostral slice
        middle      :  Value of middle slice
        caudal1     :  Value of the single most caudal slice
    """
    rostral2 = subj_cnr_all.nsmallest(2, "Slice").mean().drop("Slice")
    rostral2.index = rostral2.index + "_rostral2"
    
    avg3 = subj_cnr_all.mean().drop("Slice")
    avg3.index = avg3.index + "_avg3"
    
    max1 = subj_cnr_all.nlargest(1, 'CNR').mean().drop("Slice")
    max1.index = max1.index + "_max1"
    
    rostral1 = subj_cnr_all.nsmallest(1, "Slice").mean().drop("Slice")
    rostral1.index = rostral1.index + "_rostral1"

    middle = subj_cnr_all.iloc[1,:].drop("Slice")
    middle.index = middle.index + "_middle" 
  
    caudal1 = subj_cnr_all.nlargest(1, "Slice").mean().drop("Slice")
    caudal1.index = caudal1.index + "_caudal1"
        
    return pd.concat([rostral2, avg3, max1, rostral1, middle, caudal1])


def cnr_from_file(cnr_file):
    """
    Extracts contrast values from a given subject in base directory.
    CNR file can be passed with or without file extension.
    """
    subj_cnr_all = pd.read_csv(cnr_file, sep='\t')
    subj_cnr = summarise_cnr(subj_cnr_all)
    return subj_cnr


def get_all_subjs(filelist):
    """ Iterates over all files to extract contrast estimates and append to a dataframe """
    all_subjs_cnr = pd.DataFrame()
    for subjfile in filelist:
        subject = os.path.split(os.path.dirname(subjfile))[-1]
        subj_cnr = cnr_from_file(subjfile)
        subj_cnr = pd.DataFrame(subj_cnr, columns=[subject]).T
        all_subjs_cnr = all_subjs_cnr.append(subj_cnr)
    return all_subjs_cnr


def all_cnr_to_file(indir, cnrfile, outfile):
    """
    Searches through indir for cnrfiles and extracts LC CNR estimates.
    Saves to csv in base directory.
    """
    cnrfile = os.path.splitext(cnrfile)[0] + '.txt'
    globstr = os.path.join(indir, '*/' + cnrfile)
    filelist = glob(globstr)
    all_subjs_cnr = get_all_subjs(filelist)
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


    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        if args.outfile is None:
            outname = '_'.join([os.path.splitext(args.cnrfile)[0], "All.csv"])
            outfile = os.path.join(args.indir, outname)
        else:
            outfile = args.outfile
        ### Begin running script ###
        all_cnr_to_file(args.indir, args.cnrfile, outfile)

