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
    specificHeat = 0.9
    startTemp = 20
    orbitTime = 100
    sunlightPercent = 60
    sunlightTime = orbitTime * sunlightPercent // 100
    darkTime = orbitTime - sunlightTime
    componantP = 50
    solarPanelArea = 2000 / 10000
    solarPanelAbsorbed = 0.6
    otherArea = 500 / 10000
    otherAbsorbed = 0.01
    totalHeatRadiated = 250
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
    totalHeatRadiated = float(input("Total heat radiated in W: "))

minT = startTemp
maxT = startTemp
endT = startTemp
xPoints = []
yPoints = []
for i in range(sunlightTime):
   totalJules = (sunWPA_max + albedoWPA_max) * solarPanelArea * solarPanelAbsorbed * i
   #print(solarPanelArea)
   totalJules += (sunWPA_max + albedoWPA_max) * otherArea * otherAbsorbed * i
   totalJules += earthIRWPA_max * (solarPanelArea + otherArea) * i
   totalJules += freeMolecular_o400 * (solarPanelArea + otherArea) * i
   totalJules -= totalHeatRadiated * i
   deltaT = totalJules/(satMass*specificHeat) 
   maxT = startTemp + deltaT
   #print("Temp at minute {}: {}".format(i, str(maxT)))
   xPoints.append(i)
   yPoints.append(maxT)
for i in range(darkTime):
   totalJules = earthIRWPA_max * (solarPanelArea + otherArea) * i
   totalJules += freeMolecular_o400 * (solarPanelArea + otherArea) * i
   totalJules -= totalHeatRadiated * i
   deltaT = totalJules/satMass*specificHeat
   endT = maxT + deltaT
   #print("Temp at minute {}: {}".format(i + sunlightTime, str(endT)))
   xPoints.append(i+sunlightTime)
   yPoints.append(endT)
   

plt.plot(xPoints, yPoints)
plt.suptitle('Temperature of Satellite over Time')
plt.show()
#watts*time = q
#Jules/(mass*specificHeat) = delta(T)
