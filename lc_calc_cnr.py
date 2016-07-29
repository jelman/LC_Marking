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
import logging.config
sys.path.insert(0, '/home/jelman/netshare/K/Projects/LC_Marking/code')
from create_logger import create_logger
import lc_error_checks



def make_outfile(root, name = 'LC_CNR.txt'):
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
	Calculate locus coeruleus contrast ratio. Takes LC FSE image and mask file containing 
	ROIs of left LC (label=1), right LC (label=2), and pontine tegmentum (label=3). The 
	values of each LC ROI are averaged.
	"""
	# Load files
	img = nib.load(infile)
	img_data = img.get_data()
	mask = nib.load(mask_file)
	mask_data = mask.get_data()

	# Extract mean values from each ROI
	lLC_mean = img_data[mask_data==1].mean()
	rLC_mean = img_data[mask_data==2].mean()
	PT_mean = img_data[mask_data==3].mean()
	return lLC_mean, rLC_mean, PT_mean

def get_cnr(lLC_mean, rLC_mean, PT_mean):
	"""Calculate contrast ratio of locus coeruleus to pontine tegmentum"""
	LC_mean = (lLC_mean + rLC_mean)/2
	LC_cnr = (LC_mean - PT_mean)/PT_mean
	return LC_cnr

def save_vals(outfile, LC_cnr, lLC_mean, rLC_mean, PT_mean):
    try:
        with open(outfile, 'w') as f:
            f.write("LC_CNR\t%s\n" % LC_cnr)
            f.write("Left_LC\t%s\n" % lLC_mean)
            f.write("Right_LC\t%s\n" % rLC_mean)
            f.write("PT\t%s" % PT_mean)
    except IOError:
        print 'File could not be saved'

def cnr_to_file(infile, mask_file, outdir=None, force=False):
    if outdir==None:
        outdir, _ = os.path.split(infile)
    exists, outfile = make_outfile(outdir, 'LC_CNR.txt')
    if (exists & force==False):
        print "{} exists, delete before running or use --force flag.".format(outfile)        
        return
    logger = create_logger(outdir, name='calc_cnr.log')
    logger.info("Image file: {}".format(infile))
    logger.info("Mask file: {}".format(mask_file))
    error_status = lc_error_checks.run_error_checks(mask_file)
    lLC_mean, rLC_mean, PT_mean = get_roi_vals(infile, mask_file)
    LC_cnr = get_cnr(lLC_mean, rLC_mean, PT_mean)
    save_vals(outfile, LC_cnr, lLC_mean, rLC_mean, PT_mean)
    logger.info("Results saved to: {}".format(outfile))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""This is a  script to calculate LC CNR for a single subject and save to file.""")
    parser.add_argument('-i', '--infile', type=str, required=True, 
                        help='LC FSE file name.')
    parser.add_argument('-m', '--mask',required=True, type=str, 
                        help='Mask file name. (File containing marked ROIs)')
    parser.add_argument('-o','--outdir', required=False, 
                        help='Output directory name. (default = input file directory)')
    parser.add_argument('-f','--force', action="store_true", default=False, 
                        help='Force overwrite of existing results file (default = False)')
  
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        if args.outdir is None:
            args.outdir, _ = os.path.split(args.infile)
        ### Begin running script ###
        cnr_to_file(args.infile, args.mask, args.outdir, args.force)




