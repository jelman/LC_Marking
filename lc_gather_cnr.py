"""
After neuromelanin CNR is calculated and saved to file for each subjects, this script helps
extract and combine into a single spreadsheet. It will also produce a second spreadsheet with
the absolute difference between calculated values from each rater for each subject. This 
spreadsheet can be used to identify subjects with large differences for QC and will be named
with the suffix "_diff" appended to the output file name.
"""

import os, sys
import pandas as pd
import argparse
from glob import glob
from datetime import datetime

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


def get_all_subjs(indir):
    """
    This function takes a directory as input and returns two dataframes. The first dataframe contains the average CNR values for each subject
    and the second dataframe contains the absolute difference between the two CNR values for each subject. If more than two CNR files are found
    for a subject, a warning message is printed to the screen and appended to a log file.
    """
    tstamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = os.path.join(indir, "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, "lc_gather_cnr_{}.log".format(tstamp))
    # Initialize empty lists to hold results
    all_subjs_cnr = list()
    all_subjs_diff = list()
    # Get list of folders
    dir_list = glob(os.path.join(indir, "MRIPROC_*"))
    # Begin looping over all subject folders
    for folderpath in dir_list:
        folder = os.path.split(folderpath)[-1]
        if os.path.isdir(folderpath):
            cnr_files = glob(os.path.join(folderpath, "LC_ROI_*.txt"))
            if len(cnr_files) == 2:
                cnr1 = cnr_from_file(cnr_files[0])
                cnr2 = cnr_from_file(cnr_files[1])
                cnr = pd.DataFrame([cnr1, cnr2]).mean()
                diff = pd.DataFrame([cnr1, cnr2]).diff().abs().iloc[1]
                cnr = pd.DataFrame(cnr, columns=[folder]).T
                # Turn diff into a dataframe and transpose so that it is in the same format as cnr and folder is the index
                diff = pd.DataFrame(diff).T
                diff.index = [folder]
                # Append to list of subject data
                all_subjs_cnr.append(cnr)
                all_subjs_diff.append(diff)
                print("Success: Extracted CNR from two files for subject {}".format(folder))
                with open(log_file, "a") as f:
                    f.write("Success: Extracted CNR from two files for subject {}\n".format(folder))
            elif len(cnr_files) < 2:
                print("Warning: less than two CNR files found for subject {}".format(folder))
                with open(log_file, "a") as f:
                    f.write("Warning: less than two CNR files found for subject {}\n".format(folder))
            elif len(cnr_files) > 2:
                print("Warning: more than two CNR files found for subject {}".format(folder))
                with open(log_file, "a") as f:
                    f.write("Warning: more than two CNR files found for subject {}\n".format(folder))
    # Concatenate data from all subjects
    all_subjs_cnr = pd.conct(all_subjs_cnr)
    all_subjs_diff = pd.concat(all_subjs_diff)
    return all_subjs_cnr, all_subjs_diff


def all_cnr_to_file(indir, outfile):
    """
    Searches through indir for cnrfiles and extracts LC CNR estimates.
    Saves to csv in base directory.
    """
    all_subjs_cnr, all_subjs_diff = get_all_subjs(indir)
    diff_outfile = ''.join([os.path.splitext(outfile)[0], "_diff", os.path.splitext(outfile)[1]])
    all_subjs_cnr.to_csv(outfile, index=True, index_label='SubjectID')
    all_subjs_diff.to_csv(diff_outfile, index=True, index_label='SubjectID')


if __name__ == '__main__':


    parser = argparse.ArgumentParser(description="""
    This is a  script to gather metrics calculated for each subject. Given a base input directory, tt will 
    search all subject directories for CNR files. If it finds two files (i.e., from two raters), it will 
    average values of each metric. Averaged values across all subjects will be saved to a csv file in the 
    base directory, with the name <indir>/results/vetsa4_lc_cnr_[date].csv (unless otherwise specified). A second 
    csv file will be saved with the absolute difference between the two raters for each metric to be used
    for QC. Subjects that have less than or morethan two CNR files will be printed to the screen and appended 
    to a log in <indir>/logs/. 
    
    """)

    parser.add_argument('indir', type=str,
                        help='Directory containing subject folders')
    parser.add_argument('-o', '--outfile', type=str, required=False,
                    help='Output filename [optional]. (default=<indir>/results/vetsa4_lc_cnr_[date].csv)')


    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        if args.outfile is None:
            outdir = os.path.join(os.path.split(args.indir)[0],"results")
            outname = ''.join(["vetsa4_lc_cnr_", datetime.now().strftime("%Y-%m-%d"), ".csv"])
            outfile = os.path.join(outdir, outname)
        else:
            outfile = args.outfile
        ### Begin running script ###
        all_cnr_to_file(args.indir, outfile)

