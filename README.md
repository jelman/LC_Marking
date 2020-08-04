Code to check locus coeruleus (LC) markings for errors and calculate contrast to noise ratio (CNR). 

The images are T1 fast spin echo scans that increase the contrast of neuromelanin, a substance present in high concentrations within the LC and substantia nigra compared to surrounding tissue (Shibata et al. 2006). Images are marked according to rules described in Clewett et al. (2016), and CNR is calculated as:

  LC<sub>cnr</sub> = (LC<sub>intensity</sub> - PT<sub>intensity</sub>) / PT<sub>intensity</sub>

where LC<sub>intensity</sub> is the averaged intensity of left and right LC ROIs and PT<sub>intensity</sub> is the intensity of the pontine tegmentum. 


In the current implementation uses a modified approach in which 3 contiguous slices are marked on the LC image, and LC<sub>cnr</sub> is calculated for each slice. A per subject value can be summarized with multiple methods (e.g., maximum value only, average of all 3 slices, average of top 2 slices, average of rostral 2 slices, single most rostral slice, middle slice, and single most caudal slice). Based on findings that signal in the rostral and middle sections of the LC are associated with age (Betts et al. 2017), Alzheimer's disease, and CSF amyloid (Betts et al, 2019), the rostral 2 method is currently recommended.


User scripts:
--------------
lc_calc_cnr.py: Calculate LC<sub>cnr</sub> for a single subject.  
lc_calc_multiple_cnr.py: Calculates LC<sub>cnr</sub> for multiple subjects in a batch.  
lc_gather_cnr.py: After LC<sub>cnr</sub>  has been calculated for all subjects, this script can be used to generate a single value per subject and gathers into a spreadsheet.  


---------------

References:

Betts MJ, Cardenas-Blanco A, Kanowski M, Jessen F, Duzel E (2017): In vivo MRI assessment of the human locus coeruleus along its rostrocaudal extent in young and older adults. Neuroimage. 163:150-159.

Betts MJ, Cardenas-Blanco A, Kanowski M, Spottke A, Teipel SJ, Kilimann I, et al. (2019): Locus coeruleus MRI contrast is reduced in Alzheimer's disease dementia and correlates with CSF Abeta levels. Alzheimers Dement (Amst). 11:281-285.

Clewett DV, Lee TH, Greening S, Ponzio A, Margalit E, Mather M (2016): Neuromelanin marks the spot: identifying a locus coeruleus biomarker of cognitive reserve in healthy aging. Neurobiol Aging. 37:117-126.

Shibata E, Sasaki M, Tohyama K, Kanbara Y, Otsuka K, Ehara S, et al. (2006): Age-related changes in locus ceruleus on neuromelanin magnetic resonance imaging at 3 Tesla. Magnetic resonance in medical sciences : MRMS : an official journal of Japan Society of Magnetic Resonance in Medicine. 5:197-200.
