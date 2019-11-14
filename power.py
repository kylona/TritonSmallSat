# Initial analysis by Kyle S.
import numpy as np

otherP = 15 # 15W of power assumed for all other subsytems
solarDensity = 0.02 # 0.02 w/cm^2 
totalDutyCycle = 0.7 # 70 of total duty cycle, on over water off over land.

useConfig = (input("Use Config? (y/n): ") == "y")
if useConfig: 
    scatP = 50 # Average transmit power for the scatterometer in W
    radiP = 3 # Average power for the radiometer in W
    sunlightPercent = 60 # average time in the sun
    solarPanelArea = 1700 # roughly 42 cm x 42 cm area of solar arrays
    batteryDensity = 100 # 100mAhr/cm^3

    # orbitT = 100
    # battsize = int(input("Battery size in Whr: "))
    # maxPwr = int(input("Max Power Draw in W: "))
    # voltage = int(input("EPS voltage (usually between 2.2V - 18V): "))
else:
    scatP = int(input("Scatterometer's Ave. Power in W: "))
    radiP = int(input("Radiometer's Ave. Power in W: "))
    sunlightPercent = int(input("Time in Sunlight in percent %: "))
    solarPanelArea = int(input("Solar Panel Surface Area in cm^2: "))
    batteryDensity = 100 # 100mAhr/cm^3
    #orbitT = int(input("Orbit Time in minutes: ")) # 100
    #battsize = int(input("Battery size in Whr: "))
    #maxPwr = int(input("Max Power Draw in W: "))
    #voltage = int(input("EPS voltage (usually between 2.2V - 18V): "))


# Total Average Power = (Other) + totalDutyCycle (Scattterometer Power * scatOnTime + Radiometer Power * radiOnTime)
temp = otherP + ( scatP * 0.07 + radiP * 0.93) * totalDutyCycle
print('\nFor 7% Scatterometer usage')
print('Average Power Usage ' + str(temp))
area = temp / (sunlightPercent / 100) / solarDensity
print('Minimum Solar Area ' + str(area))

# Solved for scatOnTime in the above equation
percentage = ((solarPanelArea * solarDensity/100 * sunlightPercent) - otherP - radiP * totalDutyCycle) / ((scatP - radiP) * totalDutyCycle) * 100
print('\nScatterometer on time Percentage: ' + str(percentage))
