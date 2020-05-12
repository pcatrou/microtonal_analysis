import numpy as np

def getfilteredEnvelope (envelope,filterIntensity):
    
    filteredEnvelope = np.array([])
    for i in range(len(envelope)):
        if envelope[i]>filterIntensity:
            filteredEnvelope = np.append(filteredEnvelope, envelope[i])
        else:
            filteredEnvelope = np.append(filteredEnvelope, None)
    return filteredEnvelope

def extractMainSongLineWithMaxMethod (dbData,filteredEnvelope,timeCoef,frequencies):
    #maxValue = np.zeros(dbData.shape[1])
    maxValue = np.array([]) #a voir si c'est plus rapide?
    rev_data=dbData.transpose()
    
    for i in range(len(dbData[1])-timeCoef-1):
            ''' if (filteredEnvelope[i*timeCoef] == None):
                maxValue[i] = None
            else:
                maxValue[i] = np.argmax(rev_data[i]) '''

            if (filteredEnvelope[i*timeCoef] == None):
                maxValue =np.append(maxValue,None)
            else:
                maxValue =np.append(maxValue, np.argmax(rev_data[i]))
    maxValue = np.append(maxValue,[None,None])
    songLine = np.array([])
    for i in range(len(maxValue)):
        if (maxValue[i] != None):
            songLine = np.append(songLine,frequencies[int(maxValue[i])])
        else:
            songLine = np.append(songLine,[None])
    return songLine

def getEnvelope(ampl,delta):
    
    absAmpl = abs(ampl)
    envelope = np.array([])
    #tempEnvelope = np.array([])

    for i in range (delta,len(absAmpl),delta):
        maximum = 0
        for j in range(delta):
            maximum = max(absAmpl[i-j],maximum)
        envelope = np.append(envelope,[maximum])
    envelope = np.append(envelope,[0]) # last mesure added to fit with other data (unless lenght of envelope is missing one element)
    return envelope