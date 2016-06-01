Code to check locus coeruleus (LC) markings for errors and calculate contrast to noise ratio (CNR). 

The images are T1 fast spin echo scans that increase the contrast of neuromelanin, a substance present in high concentrations within the LC and substantia nigra compared to surrounding tissue (Shibata et al. 2006). Images are marked according to rules described in Clewett et al. (2016), and CNR is calculated as:

  LC<sub>cnr</sub> = (LC<sub>intensity</sub> - PT<sub>intensity</sub>) / PT<sub>intensity</sub>

where LC<sub>intensity</sub> is the averaged intensity of left and right LC ROIs and PT<sub>intensity</sub> is the intensity of the pontine tegmentum. 


