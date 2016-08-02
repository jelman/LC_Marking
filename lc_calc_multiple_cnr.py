"""
Takes a list of subjects and calculates neuromelanin CNR for each. These values 
are saved out to a file in each subject's directory. 
"""

import os, sys
sys.path.insert(0, '/home/jelman/netshare/VETSA_NAS/PROJ/LC_Marking/code')
import lc_calc_cnr
from glob import glob


def calc_multiple_cnr(basedir, mask_name, sublist):
	for subj in sublist:
		subjdir = os.path.join(basedir,subj)
		globstr = os.path.join(subjdir,'LC_FSE.nii*')
		infile = glob(globstr)
		if len(infile) > 1:
			raise ValueError('Multiple image files found! %s' %infile)
		else: 
			infile = infile[0]
		mask_file = os.path.join(subjdir, mask_name)
		if os.path.isfile(mask_file):
			lc_calc_cnr.cnr_to_file(infile, mask_file)
		else:
			continue

if __name__ == '__main__':


    if len(sys.argv) == 1:
        print 'Calculate CNR for a list of subjects.'
        print 'USAGE: %s <base directory name> <mask name> <subject 1> <subject 2> ...' % os.path.basename(sys.argv[0])
        print 'Outputs a csv file to base directory directory.'
    else:
        basedir = sys.argv[1]
        mask_name = sys.argv[2]
        sublist = sys.argv[3:]
        calc_multiple_cnr(basedir, mask_name, sublist)
