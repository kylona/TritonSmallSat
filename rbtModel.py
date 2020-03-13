import math
import random
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np 
from mpl_toolkits import mplot3d

time = 46
bandwidth = 100 * 10**6
T_A_min = 60
T_A_max = 160
T_rec_min = 687
T_rec_max = 1788.5

def stokes(vSig, hSig):
  Stokes = [];
  Stokes.append((vSig*vSig + hSig*hSig)/eta)
  Stokes.append((vSig*vSig - hSig*hSig)/eta)
  Stokes.append(2*np.real(vSig*np.conjugate(hSig)))
  Stokes.append(2*np.imag(vSig*np.conjugate(hSig)))
  return Stokes
  

# From Dr. Long page 295
# T_0 = 290 degrees K = the physical temperature of the antenna
# 120 < T_B = T_ML < 300
#T_ML is main lobe temp T_SL is side lobe
# T_A = 0.9 *0.8 * T_ML + 0.8*0.9*T_SL + 0.1*T_0
def rbt(wavelength, bandwidth, vSig, hSig):
  Rbt = []
  Stokes = stokes(vSig, hSig)
  for stoke in Stokes:
    Rbt.append(((wavelength**2)/(boltz*bandwidth)) * stoke)
  return Rbt

def deltaT(T_A, T_rec, bandwidth, dwelltime):
  T_sys = T_A + T_rec;
  return 2* ((T_sys) / np.sqrt(bandwidth*dwelltime)) #balanced Dicke from page 292

def T_A(V_measured, a, b):
  #main_beam = the value of interest
  #side_lobe = values received outside main beam or other polorization
  #thermal = the thermal energy emmitted by the antenna itself
  #T_A = main_beam + side_lobe + thermal

  #V_measured = a(T_A + b)
  #a = G_s the gain of the system WP-003 page 292
  #b = T_rec the temperature added by the reciever chain
  #these pyisical descriptions do not matter as a and b are captured by callibration
  T_A = (V_measured / a) - b
  return T_A

def measuredVoltage(a, T_A, b):
  return a * (T_A + b)

def computeCalibrationConstants(V_hot, T_hot, V_cold, T_cold):
  #V_hot = a(T_hot + b)
  #V_cold = a(T_cold + b)
  #V_hot - V_cold = a(T_hot - T_cold + b - b)
  a = (V_hot - V_cold)/(T_hot - T_cold)
  b = (V_cold*T_hot - V_hot*T_cold)/(V_hot - V_cold) #from WP-003 page 293
  return a, b

def printEstimatedDeltaT():
    print("Minimum Delta T: {}".format(deltaT(T_A_min,T_rec_min,bandwidth,time)))
    print("Maximum Delta T: {}".format(deltaT(T_A_max,T_rec_max,bandwidth,time)))

printEstimatedDeltaT();
