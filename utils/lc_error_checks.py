"""
This script performs error checks on LC markings. It takes the LC mask and 
tests the following rules:
1. Label 1 = right LC, Label 2 = left LC
2. PT is equidistant from each LC ROI (if odd number of slices, draw one voxel 
    closer to left LC ROI)
3. PT begins 6 voxels ventral to the most ventral LC ROI
4. LC ROIs contain 5 voxels, PT contains 100 voxels

It will also check that 3 slices are marked, and that the same 3 slices are
marked for each label.
"""

import os, sys
import nibabel as nib
import numpy as np
import logging
from utils.create_logger import create_logger
from utils.load_img_data import get_data 


def get_voxel_coords(dat, label):
    """Get voxel coordinates of a given ROI label"""
    return np.where(dat == label)


def check_nslices(z1, z2, z3):
    """
    Check that labels were marked on 3 slices testing that
    the number of unique z coords equals 3.
    If so, then will return the slice numbers (0-indexed)
    """
    assert len(np.unique(z1)) == 3
    assert len(np.unique(z2)) == 3
    assert len(np.unique(z3)) == 3
    return np.unique(z1)        

    
def check_slice_nums(z1, z2, z3):
    """
    Check that all labels were marked on the same slices by testing z coords.
    If so, then will return the slice numbers (0-indexed)
    """
    np.testing.assert_array_equal(np.unique(z1), np.unique(z2))
    np.testing.assert_array_equal(np.unique(z1), np.unique(z3))
    return np.unique(z1)        
    
    
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
        error_status = 1
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
    if (gap_left == gap_right):
        logger.debug('PT x-axis is OK')
        return error_status
    elif ((gap_right + gap_left) % 2 != 0) & (gap_left + 1 == gap_right):
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


def check_nvoxels(slice_data):
    """
    Check the number of voxels in each ROI. 
    Right LC = 5 voxels
    Left LC = 5 voxels
    PT = 100 voxels
    """
    logger = logging.getLogger(__name__)
    error_status = 0
    n_rightLC = np.sum(slice_data == 1)
    n_leftLC = np.sum(slice_data == 2)
    n_PT = np.sum(slice_data == 3)
    if (n_rightLC == 5) & (n_leftLC == 5) & (n_PT == 100):
        logger.debug('Number of voxels in all ROIs is OK')
        return error_status
    if n_rightLC != 5:
        logger.error('Right LC ROI has incorrect number of voxels!')
        error_status += 1
    if n_leftLC != 5:
        logger.error('Left LC ROI has incorrect number of voxels!')
        error_status += 1
    if n_PT != 100:
        error_status += 1
        logger.error('PT ROI has incorrect number of voxels!')
    return error_status

def check_slices(x_roi1, x_roi2, x_roi3, y_roi1, y_roi2, y_roi3, slice_data):
    error_status = 0
    error_status += check_lc_swapped(x_roi1, x_roi2)
    error_status += pt_xaxis(x_roi1, x_roi2, x_roi3)
    error_status += pt_yaxis(y_roi1, y_roi2, y_roi3)
    error_status += check_nvoxels(slice_data)
    return error_status

def run_error_checks(mask_file):
    """
    Run all error checks:
    1. Check that labels are mark on 3 slices
    2. Checked that same slices are marked for each label
    3. Check if left and right LC labels are flipped
    4. Check if PT is equidistant from each LC ROI
    5. Check if PT begins 6 voxels ventral from center of most ventral LC ROI
    6. Check if ROIs have the correct number of voxels
    """
    logger = logging.getLogger(__name__)
    mask_error_status = 0
    logger.info("Begin running error checks on mask file {}".format(mask_file))
    mask_data = get_data(mask_file)
    x_roi1_all, y_roi1_all, z_roi1_all = get_voxel_coords(mask_data, 1)
    x_roi2_all, y_roi2_all, z_roi2_all = get_voxel_coords(mask_data, 2)
    x_roi3_all, y_roi3_all, z_roi3_all = get_voxel_coords(mask_data, 3)
    try:
        nslices_ = check_nslices(z_roi1_all, z_roi2_all, z_roi3_all)
    except AssertionError:
        mask_error_status = 1
        logger.error("Labels are not marked on 3 slices, check {0}".format(mask_file))
        return mask_error_status
    try:
        slices = check_slice_nums(z_roi1_all, z_roi2_all, z_roi3_all)
    except AssertionError:
        mask_error_status = 1
        logger.error("Labels not marked on same slices, check {0}".format(mask_file))
        return mask_error_status
    for slicenum in slices:
        slice_error_status = 0
        x_roi1, y_roi1 = x_roi1_all[z_roi1_all==slicenum], y_roi1_all[z_roi1_all==slicenum]
        x_roi2, y_roi2 = x_roi2_all[z_roi2_all==slicenum], y_roi2_all[z_roi2_all==slicenum]
        x_roi3, y_roi3 = x_roi3_all[z_roi3_all==slicenum], y_roi3_all[z_roi3_all==slicenum]
        slice_data = mask_data[:,:,slicenum]
        slice_error_status += check_slices(x_roi1, x_roi2, x_roi3, y_roi1, y_roi2, y_roi3, slice_data)
        mask_error_status += slice_error_status
        if slice_error_status == 0:
            logger.info("No errors found in slice {0}".format(str(slicenum+1)))
        else:
            logger.error("{0} error(s) found, check slice {1}".format(slice_error_status, str(slicenum+1)))
    if mask_error_status == 0:
        logger.info("No errors found in {0}".format(mask_file))
    else:
        logger.error("{0} error(s) found, check {1}".format(mask_error_status, mask_file))
    return mask_error_status


if __name__ == '__main__':

    if len(sys.argv) == 1:
        print('Check the specified LC marking file for errors')
        print('USAGE: python %s <mask file>' % os.path.basename(sys.argv[0]))
        print('Rules defined in Clewett et al. (2016) NeuroImage paper')
    else:
        mask_file = sys.argv[1]
        outdir = os.path.dirname(mask_file)
        logger = create_logger(outdir, name='error_checks.log')
        run_error_checks(mask_file)
