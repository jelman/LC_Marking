# Locus Coeruleus Contrast to Noise Ratio (LC<sub>cnr</sub>) Calculation

## Overview
Code to check locus coeruleus (LC) markings for errors and calculate contrast to noise ratio (CNR). The methods are based on those described in:

Elman, J. A., et al. (2021). "MRI-assessed locus coeruleus integrity is heritable and associated with multiple cognitive domains, mild cognitive impairment, and daytime dysfunction." Alzheimer's & Dementia: The Journal of the Alzheimer's Association 17(6): 1017-1025.

The images are T1 fast spin echo scans that increase the contrast of neuromelanin, a substance present in high concentrations within the LC and substantia nigra compared to surrounding tissue (Shibata et al. 2006). Images are marked according to rules described in Clewett et al. (2016), and CNR is calculated as:

  LC<sub>cnr</sub> = (LC<sub>intensity</sub> - PT<sub>intensity</sub>) / PT<sub>intensity</sub>

where LC<sub>intensity</sub> is the averaged intensity of left and right LC ROIs and PT<sub>intensity</sub> is the intensity of the pontine tegmentum. 

In the current implementation uses a modified approach in which 3 contiguous slices are marked on the LC image, and LC<sub>cnr</sub> is calculated for each slice. The current scripts assume markings have been made using itksnap and saved to a nifti image. The following values should be used to mark each structure:
- 1 = Right LC
- 2 = Left LC
- 3 = Pontine Tegmentum

A per subject value can be summarized with multiple methods (e.g., maximum value only, average of all 3 slices, average of top 2 slices, average of rostral 2 slices, single most rostral slice, middle slice, and single most caudal slice). Based on findings that there is a rostral-caudal gradient of LC vulnerability (van Egroo et al., 2023), the rostral 2 method is currently recommended.

## Usage

The following packages:
- nibabel
- numpy
- pandas

The code is organized into 3 main scripts:
- lc_calc_cnr.py : Calculates LC<sub>cnr</sub> for a single subject.
- lc_calc_multiple_cnr.py : Wraps lc_calc_cnr.py to calculate LC<sub>cnr</sub> for multiple subjects in a batch.
- lc_gather_cnr.py : After LC<sub>cnr</sub>  has been calculated for all subjects, this script can be used to generate a single value per subject and gathers into a spreadsheet.

The scripts are designed to be run from the command line. For example, to calculate LC<sub>cnr</sub> for a single subject, the following command can be used:
``` 
python lc_calc_cnr.py -i /path/to/subject/lc_fse.nii.gz -m /path/to/subject/marking.nii.gz -o /path/to/output/directory
```

To calculate LC<sub>cnr</sub> for multiple subjects, the script assumes the same name is used for all markings. FOr example, you may wish to use each rater's initials as a filename (e.g., LC_ROI_JE.nii.gz). The following command can be used:
```
python lc_calc_multiple_cnr.py -d /path/to/data/directory -m marking_filename -s subject_list.txt -o /path/to/output/directory
```

To gather LC<sub>cnr</sub> values for all subjects into a single spreadsheet, the following command can be used:
```
python lc_gather_cnr.py /path/to/data/directory -o /path/to/output/file
```

The subject list file should be a text file with one subject per line. The data directory should contain all subject folders. Each subject folder should contain the LC image and marking image for each subject. The output directory should be the folder where files contains LC<sub>cnr</sub> and individual ROI values will be written for each subject. This defaults to the subject folder. The output file will be a spreadsheet that will contain the gathered LC<sub>cnr</sub> values for all subjects.

The scripts can be run with the -h flag to see a list of all options.

-------------------------------------------------
## References

References:

Clewett, D. V., et al. (2016). "Neuromelanin marks the spot: identifying a locus coeruleus biomarker of cognitive reserve in healthy aging." Neurobiol Aging 37: 117-126.

Elman, J. A., et al. (2021). "MRI-assessed locus coeruleus integrity is heritable and associated with multiple cognitive domains, mild cognitive impairment, and daytime dysfunction." Alzheimer's & Dementia: The Journal of the Alzheimer's Association 17(6): 1017-1025.

Van Egroo, M., et al. (2023). "Ultra-high field imaging, plasma markers and autopsy data uncover a specific rostral locus coeruleus vulnerability to hyperphosphorylated tau." Molecular Psychiatry: 1-11.

