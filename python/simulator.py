"Simple Reservoir Simulator with Effect of Rock Compressibility Change by Yohanes Nuwara"

import matplotlib.pyplot as plt
import numpy as np
from interpscal import interp

"To run this simulator, please inactivate line 20-25 of interpscal.py"

Pp_initial = 28.4 #day 1
temp = 158
max_year_inject = 5; max_day_inject = max_year_inject * 365
period = np.linspace(1, max_day_inject, 730)

bulkvol = 1E+12
porosity = 0.14
porevol = porosity * bulkvol
rhoCO2 = 0.522
injection_rate = 800

delta_Pp = 0
Pp_post_record = []
rhoCO2_record = []
KCO2_record = []
compressibility_record = []

for i in period:
    Pp_post = Pp_initial - delta_Pp
    delta_vol = 423782.1 * i
    compressibility = (interp(Pp_post)[2] * 1E-06) * (1 / 6894.76) #still in psi-1, convert to Pa-1
    delta_Pp = (1 / porevol) * (delta_vol / compressibility) / 1E+06
    Pp_post_record.append(float(Pp_post))
    # compressibility_record.append(float(compressibility))

plt.title('Pore pressure profile over production time 2014-2019')
plt.xlabel('Day')
plt.ylabel('Pressure (MPa)')
plt.xlim(1, 365*5)
plt.plot(period, Pp_post_record)
plt.savefig('Pressure_result.png')
