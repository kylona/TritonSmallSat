
otherP = 15
solarDensity = 0.02
scatP = int(input("Scatterometer's Ave. Power in W: "))
radiP = int(input("Radiometer's Ave. Power in W: "))
orbitT = int(input("Orbit Time in minutes: ")) # 100
sunlightPercent = int(input("Time in Sunlight in percent %: "))
solarPanelArea = int(input("Solar Panel Surface Area in cm^2: "))
batteryDensity = 100 # 100mAhr/cm^3
battsize = int(input("Battery size in Whr: "))
maxPwr = int(input("Max Power Draw in W: "))

temp = 15 + scatP * 0.07 + radiP * 0.93
print('Average Power Usage ' + str(temp))
area = temp / (sunlightPercent / 100) / solarDensity
print('Minimum Solar Area ' + str(area))