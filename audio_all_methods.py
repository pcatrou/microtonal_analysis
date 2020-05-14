import numpy as np

def getEnvelope(ampl,delta):
    """
    obtient l'envelope des données audio, nécessaire pour le filtre.
    """
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

def getfilteredEnvelope (envelope,intensityThreshold):
    """
    filtre les moments de silence pour un certain seuil
    """
    filteredEnvelope = np.array([])
    for i in range(len(envelope)):
        if envelope[i]>intensityThreshold:
            filteredEnvelope = np.append(filteredEnvelope, envelope[i])
        else:
            filteredEnvelope = np.append(filteredEnvelope, None)
    return filteredEnvelope

# note : faster with np.append than x[i]
def getMaxValue (dbData,filteredEnvelope,timeCoef,lowFilter):
    """
    extraction du max d'amplitude sur les données de fréquence
    ne tient pas compte des moments de silence grâce au filtrage fait sur l'envelope
    (met un None sur ces moments)
    le time coeff est le coefficient entre le nombre de points en temps sur l'envelope et sur les stft
    """

    maxValue = np.array([])
    #dbDataToFilter = dbData # to not alter dbData
    rev_data = filterHighLowFreq(dbData,lowFilter).transpose()
    #rev_data = dbData.transpose()

    for i in range(len(dbData[1])-timeCoef-1):

            if (filteredEnvelope[i*timeCoef] == None):
                maxValue =np.append(maxValue,None)
            else:
                maxValue =np.append(maxValue, int(np.argmax(rev_data[i])))
    maxValue = np.append(maxValue,[None,None])

    return maxValue

def getPitch(dbData,filteredEnvelope,timeCoef,frequencies,lowFilter):
    """
    transforme le max value (qui donne juste un indice) en données de fréquence : tableau frequencies
    """
    maxValue = getMaxValue (dbData,filteredEnvelope,timeCoef,lowFilter)
    songLine = np.array([])
    for i in range(len(maxValue)):
        if (maxValue[i] != None and maxValue[i]>10):
            songLine = np.append(songLine,frequencies[int(maxValue[i])])
        else:
            songLine = np.append(songLine,[None])
    
    return songLine


def filterHighLowFreq (stftData,lowFilter):
    """
    filtre les hautes et basses freq
    low filter : indice dans les données stft de freq a laquelle on coupe en dessous
    """
    for i in range(lowFilter): 
        stftData[i] = 0
    for i in range(len(stftData)//2):
        stftData[len(stftData)-1-i] = 0
    return stftData


def divideFreq(db,factor):
    """
    permet de diviser la fréquence des données en dB par un entier factor
    c'est la méthode pour obtenir la fondamental F_0 avec harmonic produc spectrum
    FFT(x)=FFT_O(2x)
    on passe par des transpose() car les données en freq sont sur les colonnes et non les lignes.
    """
    newDbtransp = np.ones((len(db),len(db[0]))).transpose()
    dbTransp = db.transpose()

    for f in range(len(db)//factor):
        for t in range (len(db[0])):
            newDbtransp [t][f] = dbTransp[t][factor*f]
    newDb = newDbtransp.transpose()
    return newDb

def harmonicProductSpectrum (db,iterations, coeff):
    """
    fait le produit sur un nombre d'itérations des données initiales db et celles dont la fréquence est divisée.
    un coefficient correcteur peut être ajouté (coeff) pour pondérer le HPS.
    """
    dbInit=db
    for i in range(iterations-1):
        db = (divideFreq(db,i+2))*db
    return db+coeff*dbInit
