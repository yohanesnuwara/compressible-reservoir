"Interpolation on SCAL data"

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

pressurenew = np.linspace(1, 100, 100)

def interp(pressurenew):
    # SCAL input data
    pressure_scal = np.genfromtxt('./SCAL.txt')[:,0]  # in psia
    pressure_scal = pressure_scal * 0.00689  # in MPa
    K_scal = np.genfromtxt('./SCAL.txt')[:,1]
    
    # interpolation
    tck = interpolate.splrep(pressure_scal, K_scal, s=0)
    compressibility_interp = interpolate.splev(pressurenew, tck, der=0)
    return(pressure_scal, K_scal, compressibility_interp)

## to plot the interpolated result, activate this section. If not use, inactivate this.
# pressure_scal, K_scal, c = interp(pressurenew)
# plt.plot(pressure_scal, K_scal, 'o', pressurenew, c)
# plt.title('Compressibility vs. Pressure (Fetkovich, 1998)'); plt.xlabel('Pressure (MPa)'); plt.ylabel('Compressibility')
# plt.axis([1, 70, 0, 30])
# plt.show()
