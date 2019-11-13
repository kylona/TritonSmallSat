import math
import matplotlib.pyplot as plt

sunWPA_min = 1322
sunWPA_max = 1414
albedoWPA_min = 79
albedoWPA_max = 707
earthIRWPA_min = 108
earthIRWPA_max = 332
freeMolecular_o400 = 2.25
freeMolecular_o300 = 22.5
freeMolecular_o100 = 225

useConfig = (input("Use Config? (y/n): ") == "y")
if useConfig:
    satMass = 3000
    specificHeat = 0.900
    startTemp = 20
    orbitTime = 100
    sunlightPercent = 60
    sunlightTime = orbitTime * sunlightPercent // 100
    darkTime = orbitTime - sunlightTime
    componantP_max = 50
    componantP_min = 15
    solarPanelArea = 2000 / 10000
    solarPanelAbsorbed = 0.6
    otherArea = 5000 / 10000
    otherAbsorbed = 0.01
    emissivitySolarPanels = 0.75 #http://eprints.gla.ac.uk/150163/
    emissivityOther = 0.77 #Annodized https://www.engineeringtoolbox.com/emissivity-coefficients-d_447.html
    stef_boltz = 5.6703e-8 #https://www.engineeringtoolbox.com/radiation-heat-transfer-d_431.html
    spaceTempK = 2.73
    numPeriods = 20
else:
    satMass = int(input("Mass of Satellite in grams: "))
    specificHeat = float(input("Average Specific heat of satellite: "))
    startTemp = float(input("Starting Temperature in degrees C: "))
    orbitTime = int(input("Orbit Time in minutes: "))
    sunlightPercent = int(input("Time in Sunlight in percent %: "))
    sunlightTime = orbitTime * sunlightPercent // 100
    darkTime = orbitTime - sunlightTime
    componantP = int(input("Power from Componants in Watts: "))
    solarPanelArea = int(input("Solar Panel Surface Area in cm^2: ")) / 10000
    solarPanelAbsorbed = float(input("Solar Panel Light Heat Absorption Coefficient: "))
    otherArea = int(input("Other Surface Area in cm^2: ")) / 10000
    otherAbsorbed = float(input("Other Area Light Heat Absorption Coefficient: "))

def heatRadiated(temp, emissivity, area):
  tempK = temp + 273.15
  q = emissivity * stef_boltz * (math.pow(tempK,4) - spaceTempK) * area
  return q
  
for otherArea in [500/10000,1000/10000,2000/10000,5000/10000,10000/10000,20000/10000]:
  maxXPoints = []
  maxYPoints = []
  maxT = startTemp
  totalJules = 0
  for p in range(numPeriods):
    for i in range(sunlightTime):
       deltaJules = (sunWPA_max + albedoWPA_max) * solarPanelArea * solarPanelAbsorbed
       deltaJules += (sunWPA_max + albedoWPA_max) * otherArea * otherAbsorbed
       deltaJules += earthIRWPA_max * (solarPanelArea + otherArea)
       deltaJules += freeMolecular_o400 * (solarPanelArea + otherArea)
       deltaJules += componantP_max
       deltaJules -= heatRadiated(maxT, emissivityOther, otherArea)
       deltaJules -= heatRadiated(maxT, emissivitySolarPanels, solarPanelArea)
       deltaT = deltaJules/(satMass*specificHeat) 
       maxT += deltaT
       #print("Temp at minute {}: {}".format(i, str(maxT)))
       maxXPoints.append(i + p*orbitTime)
       maxYPoints.append(maxT)
    for i in range(darkTime):
       deltaJules = earthIRWPA_max * (solarPanelArea + otherArea)
       deltaJules += freeMolecular_o400 * (solarPanelArea + otherArea)
       deltaJules += componantP_max
       deltaJules -= heatRadiated(maxT, emissivityOther, otherArea)
       deltaJules -= heatRadiated(maxT, emissivitySolarPanels, solarPanelArea)
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
       deltaJules += componantP_min
       deltaJules -= heatRadiated(minT, emissivityOther, otherArea)
       deltaJules -= heatRadiated(minT, emissivitySolarPanels, solarPanelArea)
       deltaT = deltaJules/(satMass*specificHeat) 
       minT += deltaT
       #print("Temp at minute {}: {}".format(i, str(minT)))
       minXPoints.append(i + p*orbitTime)
       minYPoints.append(minT)
    for i in range(darkTime):
       deltaJules = earthIRWPA_min * (solarPanelArea + otherArea)
       deltaJules += freeMolecular_o400 * (solarPanelArea + otherArea)
       deltaJules += componantP_min
       deltaJules -= heatRadiated(minT, emissivityOther, otherArea)
       deltaJules -= heatRadiated(minT, emissivitySolarPanels, solarPanelArea)
       deltaT = deltaJules/satMass*specificHeat
       minT += deltaT
       #print("Temp at minute {}: {}".format(i + sunlightTime, str(endT)))
       minXPoints.append(i + sunlightTime + p*orbitTime)
       minYPoints.append(minT)

  plt.plot(minXPoints, minYPoints)
  plt.plot(maxXPoints, maxYPoints)
  plt.suptitle('Temperature of Satellite over Time {} cm^2 of radiating area'.format(otherArea*10000))
  plt.xlabel('time (min)')
  plt.ylabel('Temperature Degrees C')
  plt.show()
#watts*time = q
#Jules/(mass*specificHeat) = delta(T)
