#!/bin/bash

#################################################
# Script to copy over neuromelanin scans of	#
# locus coeruleus. CHecks that scan has 8 	#
# slices and uses rsync to update folder. 	#
# Files will only overwrite if source file 	#
# is newer than target.				#
#################################################
cwd=$PWD

# Find all TSE files and check if they have 8 slices before copying over
cd /home/jelman/netshare/VETSA_NAS/mdv/4/data/MMILDB/VETSA3/proc
for i in `find . -name "TSE2D*.nii"`;
do

	if [ $(fslhd $i | grep "^dim3" | awk '{print $2'}) -eq 8 ]; then 
		rsync -RtOvu $i /home/jelman/netshare/VETSA_NAS/PROJ/LC_Marking/data; 
	fi
done

# Reorient images to standard after checking that they do not already exist
cd /home/jelman/netshare/VETSA_NAS/PROJ/LC_Marking/data
for i in `find -name "TSE2D*.nii"`; 
do 
	if [ ! -f "`dirname $i`/LC_FSE.nii.gz" ]; then
		fslreorient2std $i "`dirname $i`/LC_FSE.nii.gz"; 
	fi
done


cd $cwd


