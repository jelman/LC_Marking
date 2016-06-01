Code to check locus coeruleus (LC) markings for errors and calculate contrast to noise ratio (CNR). 

The images are T1 fast spin echo scans that increase the contrast of neuromelanin, a substance present in high concentrations within the LC and substantia nigra compared to surrounding tissue (Shibata et al. 2006). Images are marked according to rules described in Clewett et al. (2016), and CNR is calculated as:

  LC<sub>cnr</sub> = (LC<sub>intensity</sub> - PT<sub>intensity</sub>) / PT<sub>intensity</sub>

where LC<sub>intensity</sub> is the averaged intensity of left and right LC ROIs and PT<sub>intensity</sub> is the intensity of the pontine tegmentum. 


References:

Clewett, D. V., Lee, T. H., Greening, S., Ponzio, A., Margalit, E., & Mather, M. (2016). Neuromelanin marks the spot: identifying a locus coeruleus biomarker of cognitive reserve in healthy aging. Neurobiology of aging, 37, 117-126.

Sasaki, M., Shibata, E., Tohyama, K., Takahashi, J., Otsuka, K., Tsuchiya, K., ... & Sakai, A. (2006). Neuromelanin magnetic resonance imaging of locus ceruleus and substantia nigra in Parkinson's disease. Neuroreport, 17(11), 1215-1218.

