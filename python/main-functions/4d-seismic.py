"4D Seismic Simulator by Yohanes Nuwara"

import numpy as np
from simulator import simulator
from gassmann import Ks
from interpscal import interp
from Batzle_and_Wang import BW_brine_density, BW_brine_bulk, BW_gas_density, BW_gas_bulk

def rocksimulator(Pp_initial, temp, max_year_prod, bulkvol, porosity, monitor_year, salinity, \
                  SG, brine1, gas1, brine2, gas2, calc, clay, dolo, qtz, Vp, Vs, rho):

    "Matrix property calculation using Voigt-Reuss-Hill"

    # mineral elastic property database
    rhocalc = 2.71; Kcalc = 76.8; Gcalc = 32
    rhoclay = 2.58; Kclay = 20.9; Gclay = 6.9
    rhodolo = 2.87; Kdolo = 94.9; Gdolo = 45
    rhoqtz = 2.65; Kqtz = 36.6; Gqtz = 45

    mincomposition = np.array([calc, clay, dolo, qtz])
    rhomineral = np.array([rhocalc, rhoclay, rhodolo, rhoqtz])
    Kmineral = np.array([Kcalc, Kclay, Kdolo, Kqtz])
    Kmineral_inv = 1 / Kmineral
    Gmineral = np.array([Gcalc, Gclay, Gdolo, Gqtz])
    Gmineral_inv = 1 / Gmineral

    Kv = sum(mincomposition * Kmineral)
    Kr_inv = sum(mincomposition * Kmineral_inv)
    Gv = sum(mincomposition * Gmineral)
    Gr_inv = sum(mincomposition * Gmineral_inv)
    Km = (Kv+(1/Kr_inv)) / 2 #matrix bulk modulus
    Gm = (Gv+(1/Gr_inv)) / 2 #matrix shear modulus

    rhom = sum(mincomposition * rhomineral) #matrix density

    "Dry compressibility at baseline"
    c_pore1 = (interp(Pp_initial)[2] * 1E-06) * (1 / 6894.76) #pore compressibility, from psi^-1 to GPa^-1
    K_pore1 = 1 / (c_pore1 * 1E+09) #pore bulk modulus
    K_dry1 = ((1/Km)+(porosity/K_pore1))**-1 #dry bulk modulus, zimmerman (1986)
    # print(K_dry1)

    "Calculate dry compressibility at monitor year"
    c_pore2 = simulator(porosity, bulkvol, Pp_initial, max_year_prod)[1]
    period = simulator(porosity, bulkvol, Pp_initial, max_year_prod)[2]
    monitor_day = monitor_year * 365
    period_index = np.where(period == monitor_day) #find what the index of the year is
    c_pore2 = np.array(c_pore2)
    c_pore2 = c_pore2[period_index]
    K_pore2 = 1 / (c_pore2 * 1E+09)
    K_dry2 = np.float(((1/Km)+(porosity/K_pore2))**-1)
    # print(K_dry2)

    "Calculate saturated modulus and density at BASELINE"

    # saturation: 80% gas + 20% brine; initial reservoir pressure
    # fluid property calculation using Batzle-Wang (1991)
    rho_brine1 = BW_brine_density(temp, Pp_initial, salinity)
    K_brine1 = BW_brine_bulk(temp, Pp_initial, salinity, rho_brine1)
    rho_gas1 = BW_gas_density(temp, SG, Pp_initial)
    K_gas1 = BW_gas_bulk(temp, SG, Pp_initial) / 1000

    Kf_1 = 1 / ((brine1 / K_brine1) + (gas1 / K_gas1))
    rhof_1 = (brine1 * rho_brine1) + (gas1 * rho_gas1)

    #saturated modulus and density
    K_sat1 = Ks(K_dry1, Km, Kf_1, porosity) #Gassmann (1951)
    G_sat1 = rho * (Vs ** 2) / 1E+09 #according to Gassmann, shear modulus is same for all saturations, and dry
    rho_sat1 = ((1-porosity) * rhom) + (porosity * rhof_1)

    "Calculate saturated modulus and density at POST-INJECTION"

    # retrieve reservoir pressure value after injection
    Pp = simulator(porosity, bulkvol, Pp_initial, max_year_prod)[0]
    Pp = np.array(Pp)
    Pp_post = np.float(Pp[period_index])

    # saturation: 50% gas + 30% brine; initial reservoir pressure
    # fluid property calculation using Batzle-Wang (1991)

    rho_brine2 = BW_brine_density(temp, Pp_post, salinity)
    K_brine2 = BW_brine_bulk(temp, Pp_post, salinity, rho_brine2)
    rho_gas2 = BW_gas_density(temp, SG, Pp_post)
    K_gas2 = BW_gas_bulk(temp, SG, Pp_post) / 1000

    Kf_2 = 1 / ((brine2 / K_brine2) + (gas2 / K_gas2))
    rhof_2 = (brine2 * rho_brine2) + (gas2 * rho_gas2)

    #saturated modulus and density
    K_sat2 = Ks(K_dry2, Km, Kf_2, porosity) #Gassmann (1951)
    G_sat2 = G_sat1 #according to Gassmann, shear modulus is same for all saturations, and dry
    rho_sat2 = ((1-porosity) * rhom) + (porosity * rhof_2)

    "Vp, density, and Zp at baseline and post-injection"
    Vp_1 = np.sqrt((K_sat1 + (4/3 * G_sat1)) / (rho_sat1))
    Vp_2 = np.sqrt((K_sat2 + (4/3 * G_sat2)) / (rho_sat2))
    Zp_1 = (rho_sat1 * 1000) * Vp_1
    Zp_2 = (rho_sat2 * 1000) * Vp_2

    return(Vp_1, Vp_2, rho_sat1, rho_sat2, Zp_1, Zp_2)


def fourdseismic(L, f, sr, model1, model2):
    "Make Ricker wavelet"
    t = np.arange(-L / 2, L / 2 + sr, sr)

    w = 2 * np.pi * f
    ricker = (1 - 0.5 * w ** 2 * t ** 2) * np.exp(-0.25 * w ** 2 * t ** 2)
    
    "4D simulator"
    traces1 = []
    traces2 = []

    # Baseline
    for i in range(model1.shape[1]):
        seismic1 = np.convolve(ricker, model1[:, i], 'same')
        traces1.append(seismic1)
    traces1 = np.asarray(traces1).T

    # Post-injection
    for i in range(model2.shape[1]):
        seismic2 = np.convolve(ricker, model2[:, i], 'same')
        traces2.append(seismic2)
    traces2 = np.asarray(traces2).T

    return(traces1, traces2)
