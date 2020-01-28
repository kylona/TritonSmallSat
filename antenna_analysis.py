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
boltz = 1.38064852 / (10**23) #boltsman constant
pi = 3.141592654
eta = 120*pi #wave impedance of free space

xPoints = []
yPoints = []
zPoints = []

def kpc(snr, bandwidth, time):
  noise = math.sqrt( ((1 + (1/snr))*(1 + (1/snr))) + ((1/snr)*(1/snr)) )
  root_bandwidth_time = math.sqrt(bandwidth * time)
  kpc = (1/root_bandwidth_time)*noise
  return kpc

def stokes(vSig, hSig):
  Stokes = [];
  Stokes[0] = (vSig**2 + hSig**2)/eta
  Stokes[1] = (vSig**2 - hSig**2)/eta
  

def rbt(wavelength, bandwidth, vSig, hSig):
  Stokes = stokes(vSig, hSig)
  Rbt = ((wavelength**2)/(boltz*bandwidth)) * Stokes
  return Rbt

for snr in np.linspace(max_snr, min_snr):
  for bandwidth in np.linspace(max_bandwidth, min_bandwidth):
    xPoints.append(snr)  
    yPoints.append(bandwidth)  
    zPoints.append(kpc(snr,bandwidth, time))

ax = plt.axes(projection='3d')
#plt.plot(XPoints, YPoints)
ax.plot3D(xPoints, yPoints, zPoints, 'gray')
plt.suptitle('Normalized Standard Deviation (KPC')
plt.xlabel('Signal to Noise Ratio')
#ax.set_xlim(20, 1)  # decreasing time
plt.ylabel('Bandwidth')
ax.set_ylim(max_bandwidth, min_bandwidth)  # decreasing time
#red_patch = mpatches.Patch(color='Orange', label='Hot Case')
#blue_patch = mpatches.Patch(color='Blue', label='Cold Case')
#plt.legend(handles=[red_patch, blue_patch])
plt.show()
