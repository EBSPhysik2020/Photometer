import ph_MeasurementFirmware
import math
import socket

emptyintensityL = [] #doesn't change
epsilonlL = [] #doesn't change
distance = 0.0013 #doesn't change and must be > 0

def getIntensities(s, measurement_type):
    return ph_MeasurementFirmware.measureIntensity(s, measurement_type)

def doEmptyMeasurement(s, measurement_type):
    global emptyintensityL
    emptyintensityL= getIntensities(s, measurement_type)
    return emptyintensityL, 0

def doReferenceMeasurement(concentration, s, measurement_type):
    global epsilonlL
    epsilonlL = []
    if len(emptyintensityL) > 0 and concentration > 0:
        extinctionL = []
        actualintensityL = getIntensities(s, measurement_type)
    
        for i in range (3):
            extinctionL.append(math.log10(emptyintensityL[i]/actualintensityL[i]))
            epsilonlL.append(extinctionL[i] / (concentration * distance))
        return actualintensityL, extinctionL, epsilonlL, True
    else:
        return [0, 0, 0], [0, 0, 0], [0, 0, 0], False

def doOrdinaryMeasurement(s, measurement_type):
    global epsilonlL
    if len(emptyintensityL) > 0 and len(epsilonlL) > 0:
        extinctionL = []
        concentrationL = []
        actualintensityL = getIntensities(s, measurement_type)
        for i in range (3):
            extinctionL.append(round((math.log10(emptyintensityL[i]/actualintensityL[i])), 3))
            if epsilonlL[i] != 0:
                concentrationL.append(round((extinctionL[i] / (epsilonlL[i] * distance)), 3))
            else:
                print("Infinity Concentration!")
                return [0, 0, 0], [0, 0, 0], [0, 0, 0], False
        return actualintensityL, extinctionL, concentrationL, True
    else:
        return [0, 0, 0], [0, 0, 0], [0, 0, 0], False

    

    
    
    
