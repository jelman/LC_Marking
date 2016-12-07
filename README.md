Code to check locus coeruleus (LC) markings for errors and calculate contrast to noise ratio (CNR). 

The images are T1 fast spin echo scans that increase the contrast of neuromelanin, a substance present in high concentrations within the LC and substantia nigra compared to surrounding tissue (Shibata et al. 2006). Images are marked according to rules described in Clewett et al. (2016), and CNR is calculated as:

  LC<sub>cnr</sub> = (LC<sub>intensity</sub> - PT<sub>intensity</sub>) / PT<sub>intensity</sub>

where LC<sub>intensity</sub> is the averaged intensity of left and right LC ROIs and PT<sub>intensity</sub> is the intensity of the pontine tegmentum. 

In the current implementation, 3 contiguous slices are marked on the LC image, and LC<sub>cnr</sub> is calculated for each slice. A per subject value can be summarized with multiple methods (e.g., maximum value only, average of all 3 slices, average of top 2 slices). 

User scripts:
--------------
lc_calc_cnr.py: Calculate LC<sub>cnr</sub> for a single subject.  

lc_calc_multiple_cnr.py: Calculates LC<sub>cnr</sub> for multiple subjects in a batch.  

lc_gather_cnr.py: After LC<sub>cnr</sub>  has been claculated for all subjects, this script can be used to generate a single value per subject and gathers into a spreadsheet.  

---------------

References:

Clewett, D. V., Lee, T. H., Greening, S., Ponzio, A., Margalit, E., & Mather, M. (2016). Neuromelanin marks the spot: identifying a locus coeruleus biomarker of cognitive reserve in healthy aging. Neurobiology of aging, 37, 117-126.

Sasaki, M., Shibata, E., Tohyama, K., Takahashi, J., Otsuka, K., Tsuchiya, K., ... & Sakai, A. (2006). Neuromelanin magnetic resonance imaging of locus ceruleus and substantia nigra in Parkinson's disease. Neuroreport, 17(11), 1215-1218.


