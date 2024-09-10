# Locus Coeruleus Contrast to Noise Ratio (LC<sub>cnr</sub>) Calculation

## Overview
Code to check locus coeruleus (LC) markings for errors and calculate contrast to noise ratio (LC<sub>cnr</sub>). The methods are based on those described in:

Elman, J. A., et al. (2021). "MRI-assessed locus coeruleus integrity is heritable and associated with multiple cognitive domains, mild cognitive impairment, and daytime dysfunction." Alzheimer's & Dementia: The Journal of the Alzheimer's Association 17(6): 1017-1025.

The images are T1 fast spin echo scans that increase the contrast of neuromelanin, a substance present in high concentrations within the LC and substantia nigra compared to surrounding tissue (Shibata et al. 2006). Images are marked according to rules described in Elman et al. (2016), and are based on resules originally described in Clewett et al. (2016).  LC<sub>cnr</sub> is calculated as:

  LC<sub>cnr</sub> = (LC<sub>intensity</sub> - PT<sub>intensity</sub>) / PT<sub>intensity</sub>

where LC<sub>intensity</sub> is the averaged intensity of left and right LC ROIs and PT<sub>intensity</sub> is the intensity of the pontine tegmentum. 

In the current implementation uses a modified approach in which 3 contiguous slices are marked on the LC image, and LC<sub>cnr</sub> is calculated for each slice. The current scripts assume markings have been made using itksnap and saved to a nifti image. The following values should be used to mark each structure:
- 1 = Right LC
- 2 = Left LC
- 3 = Pontine Tegmentum

A per subject value can be summarized with multiple methods (e.g., maximum value only, average of all 3 slices, average of top 2 slices, average of rostral 2 slices, single most rostral slice, middle slice, and single most caudal slice). Based on findings that there is a rostral-caudal gradient of LC vulnerability (van Egroo et al., 2023), the rostral 2 method is currently recommended.

These scripts additionally assume that two raters mark each image. The final CNR values are obtained by averaging across raters. For QC purposes, a file containing the differences in CNR values between raters will also be produced. This file can be checked for large discrepancies that may indicate an error in marking or need for harmonization in marking rules. 

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

*Note for internal VETSA use: The copy_reorient.sh script must be run to prior to marking. Raw dicom data is converted to mgz as part of the CMIG processing pipeline. The mgz files are copied to the VETSA NAS, converted to nifti, and reoriented to standard orientation. These re-oriented nifti files are used for marking. Paths are hard-coded, so ensure they are correct prior to use.*

-------------------------------------------------
## References

References:

Clewett, D. V., Lee, T. H., Greening, S., Ponzio, A., Margalit, E., & Mather, M. (2016). Neuromelanin marks the spot: identifying a locus coeruleus biomarker of cognitive reserve in healthy aging. Neurobiol Aging, 37, 117-126. doi:10.1016/j.neurobiolaging.2015.09.019

Elman, J. A., Puckett, O. K., Beck, A., Fennema-Notestine, C., Cross, L. K., Dale, A. M., Eglit, G. M. L., Eyler, L. T., Gillespie, N. A., Granholm, E. L., Gustavson, D. E., Hagler, D. J., Jr., Hatton, S. N., Hauger, R., Jak, A. J., Logue, M. W., McEvoy, L. K., McKenzie, R. E., Neale, M. C., Panizzon, M. S., Reynolds, C. A., Sanderson-Cimino, M., Toomey, R., Tu, X. M., Whitsel, N., Williams, M. E., Xian, H., Lyons, M. J., Franz, C. E., & Kremen, W. S. (2021). MRI-assessed locus coeruleus integrity is heritable and associated with multiple cognitive domains, mild cognitive impairment, and daytime dysfunction. Alzheimer's & Dementia: The Journal of the Alzheimer's Association, 17(6), 1017-1025. doi:10.1002/alz.12261

Shibata, E., Sasaki, M., Tohyama, K., Kanbara, Y., Otsuka, K., Ehara, S., & Sakai, A. (2006). Age-related changes in locus ceruleus on neuromelanin magnetic resonance imaging at 3 Tesla. Magn Reson Med Sci, 5(4), 197-200. 

Van Egroo, M., Riphagen, J. M., Ashton, N. J., Janelidze, S., Sperling, R. A., Johnson, K. A., Yang, H. S., Bennett, D. A., Blennow, K., Hansson, O., Zetterberg, H., & Jacobs, H. I. L. (2023). Ultra-high field imaging, plasma markers and autopsy data uncover a specific rostral locus coeruleus vulnerability to hyperphosphorylated tau. Molecular Psychiatry, 1-11. doi:10.1038/s41380-023-02041-y

