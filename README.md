# compressible-reservoir

**compressible-reservoir** is a Python simulator that simulates the effect of rock compressibility in reservoir simulation and 4D seismic. 

Rock compressibility (Cr) in rocks changes linearly and non-linearly with reservoir pressure (Chertov & Suarez-Rivera, 2014). Linear behavior is typical to low porosity and highly-consolidated rock, whereas non-linear behavior is typical to high porosity and weakly-consolidated rock. In most simulation cases, the effect of changing rock compressibility is often neglected, so the Cr is kept constant. This simulator shows that both these linear and non-linear behaviour of Cr affects the depletion of reservoir pressure after production. We can also study using this simulator, about compaction drive mechanism.

**compressible-reservoir** is also a time-lapse (4D) seismic simulator that simulates seismic response change, of course due to changing rock compressibility, and changing oil/gas saturation, in a simple synthetic geological model. 

**Assumptions made:** homogeneous reservoir, only time dimension (no spatial), no phase flow.  

**Input data:**
SCAL_linear.txt     : SCAL data of linear Cr change (sandstone dataset of Gulf Coast by Fetkovitch et al, 1998) <br/>
SCAL_nonlinear.txt  : SCAL data of non-linear Cr change (sandstone dataset by Zimmerman, 1986)
faultedchannel.txt  : synthetic faulted channel for 4D seismic modelling

**Main functions:**
simulator.py        : pressure simulator using simple equation
4Dseismic.py        : time-lapse/4D seismic response modelling

**Support Functions:**
interpscal.py       : interpolating SCAL data
batzlewang.py       : rock physics function; Batzle-Wang (1991) to predict water, oil, and gas properties 
gassmann.py         : rock physics function; Gassmann (1951) to predict elastic properties of the saturated sandstone
Kuster_Toksoz.py    : rock physics function; Kuster-Toksoz (1973) to predict elastic properties of the saturated carbonate
DEM.py              : rock physics function; Differential Effective Medium by Berryman (1980) to predict elastic properties of saturated rock

**Test Programs:**
simulator-test.py   : reservoir pressure simulation using dataset of non-linear and linear SCAL, and to compare the effect of constant Cr and changing Cr to pressure result
4Dseismic-test.py   : time-lapse seismic response of produced oil/gas from a faulted channel model

**Output:**
InterpolatedSCAL.png          : result of interpolated SCAL data
Pressure_Result_Initial_28MPa : result of reservoir pressure if the initial reservoir pressure is 28 MPa (normal sandstone)
Pressure_Result_Initial_55MPa : result of reservoir pressure if the initial reservoir pressure is 55 MPa (high pressurized sandstone, case of Gulf Coast)
Time-lapse.png                : result of baseline (pre-production), post-production seismic image, and the difference seismic image. 

**What's next?**
**compressible-reservoir** will be continuously developed to account for phase flow, started from single-phase flow in 1D, 2D, to larger dimension. Also it will offer compatibility to make own synthetic models, and even import geological model to this simulator. Geomechanics function will be added. The rock physics function will be also more advanced. This next step is commonly regarded as Petro-elastic Modelling (PEM). 

With all my regards, may you enjoy this simulation, and don't forget to take into account the importance of rock compressibility behaviour in reservoir simulation!

**Yohanes Nuwara**
