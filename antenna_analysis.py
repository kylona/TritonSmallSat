import math
import random
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np 
from mpl_toolkits import mplot3d


time = 1/1000
max_bandwidth = 100 * 10**6
min_bandwidth = 1000
max_snr = 800
min_snr = 1
max_wavelength = 25 / (10**3)
min_wavelength = 16.7 / (10**3)
boltz = 1.38064852 / (10**23) #boltsman constant
pi = 3.141592654
eta = 120*pi #wave impedance of free space


def kpc(snr, bandwidth, time):
  noise = math.sqrt( ((1 + (1/snr))*(1 + (1/snr))) + ((1/snr)*(1/snr)) )
  root_bandwidth_time = math.sqrt(bandwidth * time)
  kpc = (1/root_bandwidth_time)*noise
  return kpc

def stokes(vSig, hSig):
  Stokes = [];
  Stokes.append((vSig*vSig + hSig*hSig)/eta)
  #Stokes.append((vSig*vSig - hSig*hSig)/eta)
  #Stokes.append(2*np.real(vSig*np.conjugate(hSig)))
  #Stokes.append(2*np.imag(vSig*np.conjugate(hSig)))
  return Stokes
  

def rbt(wavelength, bandwidth, vSig, hSig):
  Rbt = []
  Stokes = stokes(vSig, hSig)
  for stoke in Stokes:
    Rbt.append(((wavelength**2)/(boltz*bandwidth)) * stoke)
  return Rbt

def deltaT(T_A, T_rec, bandwidth, dwelltime):
  T_sys = T_A + T_rec;
  return (T_sys) / np.sqrt(bandwidth*dwelltime)

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

xPoints = []
yPoints = []
zPoints = []

for wavelength in np.linspace(max_wavelength, min_wavelength):
  for bandwidth in np.linspace(max_bandwidth, min_bandwidth):
    xPoints.append(wavelength)  
    yPoints.append(bandwidth)  
    zPoints.append(rbt(wavelength, bandwidth, 1, 1)[0]) #TODO make vSig and hSig better

ax = plt.axes(projection='3d')
#plt.plot(XPoints, YPoints)
ax.plot3D(xPoints, yPoints, zPoints, 'gray')
plt.suptitle('Radiometric Brightness Temperatrue (RBT)')
plt.xlabel('Wavelength')
#ax.set_xlim(20, 1)  # decreasing time
plt.ylabel('Bandwidth')
ax.set_ylim(max_bandwidth, min_bandwidth)  # decreasing time
#red_patch = mpatches.Patch(color='Orange', label='Hot Case')
#blue_patch = mpatches.Patch(color='Blue', label='Cold Case')
#plt.legend(handles=[red_patch, blue_patch])
plt.show()
