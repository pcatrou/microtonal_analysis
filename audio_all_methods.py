import numpy as np

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

def getfilteredEnvelope (envelope,filterIntensity):
    
    filteredEnvelope = np.array([])
    for i in range(len(envelope)):
        if envelope[i]>filterIntensity:
            filteredEnvelope = np.append(filteredEnvelope, envelope[i])
        else:
            filteredEnvelope = np.append(filteredEnvelope, None)
    return filteredEnvelope

# note : faster with np.append than x[i]
def getMaxValue (dbData,filteredEnvelope,timeCoef):

    maxValue = np.array([])
    #dbDataToFilter = dbData # to not alter dbData
    rev_data = filterHighLowFreq(dbData).transpose()
    #rev_data = dbData.transpose()

    for i in range(len(dbData[1])-timeCoef-1):

            if (filteredEnvelope[i*timeCoef] == None):
                maxValue =np.append(maxValue,None)
            else:
                maxValue =np.append(maxValue, int(np.argmax(rev_data[i])))
    maxValue = np.append(maxValue,[None,None])

    return maxValue

def extractMainSongLineWithMaxMethod(dbData,filteredEnvelope,timeCoef,frequencies):
    maxValue = getMaxValue (dbData,filteredEnvelope,timeCoef)
    songLine = np.array([])
    for i in range(len(maxValue)):
        if (maxValue[i] != None and maxValue[i]>10):
            songLine = np.append(songLine,frequencies[int(maxValue[i])])
        else:
            songLine = np.append(songLine,[None])
    
    return songLine

def filterHighLowFreq (stftData):
    for i in range(24): #TODO passer en paramètres les valeurs de filtres... (celles qui marchaient pour lea : 24, 2)
        stftData[i] = 0
    for i in range(len(stftData)//2):
        stftData[len(stftData)-1-i] = 0
    return stftData


def divideFreq(db,factor):
    newDbtransp = np.ones((len(db),len(db[0]))).transpose()
    dbTransp = db.transpose()

    for f in range(len(db)//factor):
        for t in range (len(db[0])):
            newDbtransp [t][f] = dbTransp[t][factor*f]
    newDb = newDbtransp.transpose()
    return newDb

def harmonicProductSpectrum (db,iterations, coeff):
    dbInit=db
    for i in range(1,iterations):
        db = db*(divideFreq(db,i+1))
    return db+coeff*dbInit
