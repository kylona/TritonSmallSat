import math
import random
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np 
from mpl_toolkits import mplot3d

requiredKPC = 0.01582
numLooks = 4
time = 1/25
bandwidth = 25 * (10**3)
adc_enob = 8

def kpc(snr, bandwidth, time):
  noise = math.sqrt(((1 + (1/snr))*(1 + (1/snr))) + ((1/snr)*(1/snr)) )
  root_bandwidth_time = np.sqrt(bandwidth * time)
  kpc = (1/root_bandwidth_time)*noise
  return kpc

def computeRequiredSNR(kpc, bandwidth, time):
  reqSNR = (np.sqrt(2*bandwidth*kpc*kpc*time-1) + 1)/(bandwidth*kpc*kpc*time-1)
  return reqSNR


def printSNRComponantRequirements(snr):
  print("SYSTEM SNR: ", str(20*np.log10(snr)), " dB")
  adc_snr = 6.02 * adc_enob + 1.76
  print("ADC SNR: ", adc_snr, " dB")
  adc_snr = 10**(adc_snr/20)
  print("REMAINING SNR: ", 20*np.log10(1/(1/snr - 1/adc_snr)), " dB")

printSNRComponantRequirements(computeRequiredSNR(requiredKPC, bandwidth, numLooks*time))
  

