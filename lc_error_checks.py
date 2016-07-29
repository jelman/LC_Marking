"""
This script performs error checks on LC markings. It takes the LC mask and 
tests the following rules:
1. Label 1 = right LC, Label 2 = Right LC
2. PT is equidistant from each LC ROI (if odd number of slices, draw one voxel 
    closer to left LC ROI)
3. PT begins 6 voxels ventral to the most ventral LC ROI
4. LC ROIs contain 5 voxels, PT contains 100 voxels
"""

import os, sys
import nibabel as nib
import numpy as np
import logging


def get_data(infile):
    """Load image and return data matrix"""
    logger = logging.getLogger(__name__)
    img = nib.load(infile)
    img_data = img.get_data()
    logger.debug("Loaded {}".format(infile))
    return img_data

def get_voxel_coords(dat, label):
    """Get voxel coordinates of a given ROI label"""
    return np.where(dat==label)
 

def check_lc_swapped(x_rightLC, x_leftLC):
    """
    Check if the LC ROI labels are swapped.  
    1 = Right LC
    2 = Left LC
    """
    logger = logging.getLogger(__name__)    
    error_status = 0
    if all([all(x > x_leftLC) for x in x_rightLC]):
        error_status = 0
        logger.debug('Left and Right LC Labels OK')
        return error_status
    else:
        error_status=1
        logger.error('Left and Right LC ROIs are flipped!')
        return error_status
    
def pt_xaxis(x_rightLC, x_leftLC, x_PT):
    """
    Check PT placement along x-axis. The PT should be equidistant from left 
    and right LC ROIs. If there are an odd number of voxels, place PT one 
    voxel closer to the left LC ROI.
    """
    logger = logging.getLogger(__name__)    
    error_status = 0
    gap_right = x_rightLC.min() - x_PT.max()
    gap_left = x_PT.min() - x_leftLC.max()
    if (gap_left==gap_right):
        logger.debug('PT x-axis is OK')
        return error_status
    elif ((gap_right + gap_left) % 2 != 0) & (gap_left+1 == gap_right):
        logger.debug('PT x-axis is OK')
        return error_status
    else:
        logger.error('PT is not equidistant from LC ROIs!')
        error_status = 1
        return error_status

def pt_yaxis(y_rightLC, y_leftLC, y_PT):
    """
    Check placement of PT along the y-axis. The boundary of the PT should 
    begin 6 voxels ventral from the center of the most ventral LC ROI.
    """
    logger = logging.getLogger(__name__)    
    error_status = 0
    ventralLC = int(max(np.median(y_rightLC), np.median(y_leftLC)))    
    if (y_PT.min() - ventralLC) == 6:
        logger.debug('PT y-axis is OK')
        return error_status
    else:
        logger.error('PT is not 6 voxels ventral to most ventral LC!')
        error_status = 1
        return error_status
        
def check_nvoxels(mask_data):
    """
    Check the number of voxels in each ROI. 
    Right LC = 5 voxels
    Left LC = 5 voxels
    PT = 100 voxels
    """
    logger = logging.getLogger(__name__)    
    error_status = 0
    n_rightLC = np.sum(mask_data==1)
    n_leftLC = np.sum(mask_data==2)
    n_PT = np.sum(mask_data==3)
    if (n_rightLC==5) & (n_leftLC==5) & (n_PT==100):
        logger.debug('Number of voxels in all ROIs is OK')
        return error_status        
    if n_rightLC!=5:
        logger.error('Right LC ROI has incorrect number of voxels!')
        error_status+=1
    if n_leftLC!=5:
        logger.error('Left LC ROI has incorrect number of voxels!')    
        error_status+=1
    if n_PT!=100:
        error_status+=1
        logger.error('PT ROI has incorrect number of voxels!')
    return error_status  

def run_error_checks(mask_file):
    """
    Run all error checks:
    1. Check if left and right LC labels are flipped
    2. Check if PT is equidistant from each LC ROI
    3. Check if PT begins 6 voxels ventral from center of most ventral LC ROI
    4. Check if ROIs have the correct number of voxels
    """
    logger = logging.getLogger(__name__)
    error_status = 0
    logger.info("Begin running error checks on mask file {}".format(mask_file))
    mask_data = get_data(mask_file)
    x_roi1, y_roi1, z_roi1 = get_voxel_coords(mask_data, 1)
    x_roi2, y_roi2, z_roi2 = get_voxel_coords(mask_data, 2)
    x_roi3, y_roi3, z_roi3 = get_voxel_coords(mask_data, 3)    
    error_status += check_lc_swapped(x_roi1, x_roi2)
    error_status += pt_xaxis(x_roi1, x_roi2, x_roi3)
    error_status += pt_yaxis(y_roi1, y_roi2, y_roi3)
    error_status += check_nvoxels(mask_data)
    if error_status==0:
        logger.info('No errors found in mask file')
    else:
        logger.error("{0} error(s) found, check {1}".format(error_status, mask_file))
    return error_status

            
def create_logger(outdir, name=None):
    # create logger 
    #logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    if not name:
        name = 'error_checks.log'
    logfile = os.path.join(outdir, name)
    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.INFO)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger         
    
if __name__ == '__main__':


    if len(sys.argv) == 1:
        print 'Check the specified LC marking file for errors'
        print 'USAGE: python %s <mask file>' % os.path.basename(sys.argv[0])
        print 'Rules defined in Clewett et al. (2016) NeuroImage paper'
    else:
        mask_file = sys.argv[1]
        outdir = os.path.dirname(mask_file)
        logger = create_logger(outdir)
        run_error_checks(mask_file)