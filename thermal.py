import math
import random
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

sunWPA_min = 1322 #minimum power from sunlight in watts per m^2
sunWPA_max = 1414 #maximum power from sunlight in watts per m^2
albedoWPA_min = 79 #minimum power reflected from earth in watts per m^2
albedoWPA_max = 707 #maximum power reflected from earth in watts per m^2
earthIRWPA_min = 108 #minimum power radiated from earth as infrared in watts per m^2
earthIRWPA_max = 332 #maximum power radiated from earth as infrared in watts per m^2
freeMolecular_o400 = 2.25 #heat generated from collision with free air molecules in watts per m^2
freeMolecular_o300 = 22.5 # ^ but at 300 km altitude
freeMolecular_o100 = 225 # ^ but at 100 km altitude

satMass = 4000 #Arbitrary 4 kg weight
specificHeat = 0.900 #specific heat of aluminum
startTemp = 20 #Arbitrary start temp in degrees C
orbitTime = 100 #Arbitrary value in minutes
sunlightPercent = 60 # % of time in sunlight
sunlightTime = orbitTime * sunlightPercent // 100 #compute sunlight time in minutes
darkTime = orbitTime - sunlightTime #compute dark time in minutes
totalSolarArea = 3600 / 10000 #total area of satellite made of solar panel
solarPanelArea = 1024 / 10000 #area of solar panel in sun in m^2. (thought of as cm^2)
solarDarkArea = totalSolarArea - solarPanelArea #area of solar panel in shadow in m^2. (thought of as cm^2)
solarPanelAbsorbed = 0.7 #proportion of power from sunlight absorbed as heat by solar panels
                         #https://www.pveducation.org/pvcdrom/materials/optical-properties-of-silicon
otherArea = 500 / 10000 #Non-solar-panel area
otherAbsorbed = 0.01 #proportion of power from sunlight absorbed as heat by non-solar-panels
emissivitySolarPanels = 0.75 #http://eprints.gla.ac.uk/150163/
emissivityOther = 0.77 #Annodized https://www.engineeringtoolbox.com/emissivity-coefficients-d_447.html
stef_boltz = 5.6703e-8 #https://www.engineeringtoolbox.com/radiation-heat-transfer-d_431.html
spaceTempK = 2.73 #From google temperature of space in Kelvin
numPeriods = 100 #the number of orbits to include in output
componantP = 15 # power lost to heat from provided componants
percentScatTime = 7/100 #percent of time we need to run scaterometry
percentOperating_max = 100/100
percentOperating_min = 50/100

def heatRadiated(temp, emissivity, area):
  tempK = temp + 273.15 #convert from C to K
  q = emissivity * stef_boltz * (math.pow(tempK,4) - math.pow(spaceTempK,4)) * area
  #https://www.engineeringtoolbox.com/radiation-heat-transfer-d_431.html
  return q

def componantHeatMax(time):
  scat_maxP = 150 #max scaterometry 
  radiometry_maxP = 10 #max radiometry power lost to heat
  deltaJules = 0
  if (time <= percentOperating_max*orbitTime): #bias power on in sunlight
    deltaJules += radiometry_maxP
    if (time <= orbitTime*percentScatTime):
      deltaJules += scat_maxP
  return deltaJules

def componantHeatMin(time):
  scat_minP = 50 #min scaterometry power lost to heat
  radiometry_minP = 3 #min radiometry power lost to heat
  deltaJules = 0
  if (time >= percentOperating_min*orbitTime): #bias power off in darkness
    deltaJules += radiometry_minP
    if (time <= orbitTime*percentScatTime):
      deltaJules += scat_minP
  return 15
  
  
for solarPanelArea in [936.4/10000, 1936.4/10000, 200/10000]:
  solarDarkArea = totalSolarArea - solarPanelArea #area of solar panel in shadow in m^2. (thought of as cm^2)
  maxXPoints = []
  maxYPoints = []
  maxT = startTemp
  totalJules = 0
  for p in range(numPeriods):
    for i in range(sunlightTime):
       #compute net change in jules per minute
       deltaJules = (sunWPA_max + albedoWPA_max) * solarPanelArea * solarPanelAbsorbed
       deltaJules += (sunWPA_max + albedoWPA_max) * otherArea * otherAbsorbed
       deltaJules += earthIRWPA_max * (solarPanelArea + otherArea)
       deltaJules += freeMolecular_o400 * (solarPanelArea + otherArea)
       deltaJules += componantHeatMax(i)
       deltaJules -= heatRadiated(maxT, emissivityOther, otherArea)
       deltaJules -= heatRadiated(maxT, emissivitySolarPanels, solarPanelArea)
       deltaJules -= heatRadiated(maxT, emissivitySolarPanels, solarDarkArea)
       deltaT = deltaJules/(satMass*specificHeat) 
       maxT += deltaT
       #print("Temp at minute {}: {}".format(i, str(maxT)))
       maxXPoints.append(i + p*orbitTime)
       maxYPoints.append(maxT)
    for i in range(darkTime):
       deltaJules = earthIRWPA_max * (solarPanelArea + otherArea)
       deltaJules += freeMolecular_o400 * (solarPanelArea + otherArea)
       deltaJules += componantHeatMax(i+sunlightTime)
       deltaJules -= heatRadiated(maxT, emissivityOther, otherArea)
       deltaJules -= heatRadiated(maxT, emissivitySolarPanels, solarPanelArea)
       deltaJules -= heatRadiated(maxT, emissivitySolarPanels, solarDarkArea)
       deltaT = deltaJules/satMass*specificHeat
       maxT += deltaT
       #print("Temp at minute {}: {}".format(i + sunlightTime, str(endT)))
       maxXPoints.append(i + sunlightTime + p*orbitTime)
       maxYPoints.append(maxT)
  minXPoints = []
  minYPoints = []
  minT = startTemp
  totalJules = 0
  for p in range(numPeriods):
    for i in range(sunlightTime):
       deltaJules = (sunWPA_min + albedoWPA_min) * solarPanelArea * solarPanelAbsorbed
       deltaJules += (sunWPA_min + albedoWPA_min) * otherArea * otherAbsorbed
       deltaJules += earthIRWPA_min * (solarPanelArea + otherArea)
       deltaJules += freeMolecular_o400 * (solarPanelArea + otherArea)
       deltaJules += componantHeatMin(i)
       deltaJules -= heatRadiated(minT, emissivityOther, otherArea)
       deltaJules -= heatRadiated(minT, emissivitySolarPanels, solarPanelArea)
       deltaJules -= heatRadiated(minT, emissivitySolarPanels, solarDarkArea)
       deltaT = deltaJules/(satMass*specificHeat) 
       minT += deltaT
       #print("Temp at minute {}: {}".format(i, str(minT)))
       minXPoints.append(i + p*orbitTime)
       minYPoints.append(minT)
    for i in range(darkTime):
       deltaJules = earthIRWPA_min * (solarPanelArea + otherArea)
       deltaJules += freeMolecular_o400 * (solarPanelArea + otherArea)
       deltaJules += componantHeatMin(i+sunlightTime)
       deltaJules -= heatRadiated(minT, emissivityOther, otherArea)
       deltaJules -= heatRadiated(minT, emissivitySolarPanels, solarPanelArea)
       deltaJules -= heatRadiated(minT, emissivitySolarPanels, solarDarkArea)
       deltaT = deltaJules/satMass*specificHeat
       minT += deltaT
       #print("Temp at minute {}: {}".format(i + sunlightTime, str(endT)))
       minXPoints.append(i + sunlightTime + p*orbitTime)
       minYPoints.append(minT)

  plt.plot(minXPoints, minYPoints)
  plt.plot(maxXPoints, maxYPoints)
  plt.suptitle('Temperature of 3U Satellite over Time')
  plt.xlabel('time (min)')
  plt.ylabel('Temperature Degrees C')
  red_patch = mpatches.Patch(color='Orange', label='Hot Case')
  blue_patch = mpatches.Patch(color='Blue', label='Cold Case')
  plt.legend(handles=[red_patch, blue_patch])
  plt.show()
#watts*time = q
#Jules/(mass*specificHeat) = delta(T)
