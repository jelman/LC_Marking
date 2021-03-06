#!/bin/bash

#################################################
# Script to copy over neuromelanin scans of	#
# locus coeruleus. CHecks that scan has 8 	#
# slices and uses rsync to update folder. 	#
# Files will only overwrite if source file 	#
# is newer than target.				#
#################################################
cwd=$PWD
PATH=/bin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:/usr/lib/fsl/5.0:/usr/local/freesurfer/bin/
. /etc/fsl/fsl.sh


copy_fname="copy_reorient_"`date +%F`".log"

# Find all TSE files and check if they have 8 slices before copying over

cd "/home/vetsatwinstudy/netshare/SYNVETSACOPY/data/vetsa/VETSA3_FS51_DTI232/proc"
for i in `find . -name "TSE2D*.mgz"`;
do
    nslices=$(mri_info $i --nslices)
	if [ $nslices -ge 5 ] && [ $nslices -le 8 ]; then 
		rsync -RtOvu $i "/home/vetsatwinstudy/netshare/M/PSYCH/KREMEN/VETSA 3 MRI/LC_Marking/data" >> "/home/vetsatwinstudy/netshare/M/PSYCH/KREMEN/VETSA 3 MRI/LC_Marking/data/logs/$copy_fname"; 
	fi
done

# Convert images to nifti if they do not already exist
cd "/home/vetsatwinstudy/netshare/M/PSYCH/KREMEN/VETSA 3 MRI/LC_Marking"
for i in `find -name "TSE2D*.mgz"`; 
do 
	if [ ! -f ${i%.mgz}".nii" ]; then
		mri_convert $i ${i%.mgz}".nii"; 
	fi
done
# Reorient images to standard after checking that they do not already exist
cd "/home/vetsatwinstudy/netshare/M/PSYCH/KREMEN/VETSA 3 MRI/LC_Marking"
for i in `find -name "TSE2D*.nii"`; 
do 
	if [ ! -f "`dirname $i`/LC_FSE.nii.gz" ]; then
		fslreorient2std $i "`dirname $i`/LC_FSE.nii.gz"; 
	fi
done


cd "$cwd"


