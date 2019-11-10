"Interpolation on SCAL data"

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

pressurenew = np.linspace(1, 100, 100)

def interp(pressurenew):
    pressure_northsea = np.genfromtxt('./SCAL.txt')[:,0]  # in psia
    pressure_northsea = pressure_northsea * 0.00689  # in MPa
    compressibility_northsea = np.genfromtxt('./SCAL.txt')[:,1]
    tck = interpolate.splrep(pressure_northsea, compressibility_northsea, s=0)
    compressibility_interp = interpolate.splev(pressurenew, tck, der=0)
    return(pressure_northsea, compressibility_northsea, compressibility_interp)

pressure_northsea, compressibility_northsea, c = interp(pressurenew)
plt.plot(pressure_northsea, compressibility_northsea, 'o', pressurenew, c)
plt.title('Compressibility vs. Pressure (Fetkovich, 1998)'); plt.xlabel('Pressure (MPa)'); plt.ylabel('Compressibility')
plt.axis([1, 70, 0, 30])
plt.show()
