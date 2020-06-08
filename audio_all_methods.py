import numpy as np

def getEnvelope(ampl,timeCoeff):
    """
    Get the amplitude envelope of audio data. the time indent is changed to timeCoeff
    
    Parameters:
    ampl,timeCoeff
    
    Returns:
    filteredEnvelope
    """
    absAmpl = abs(ampl)
    envelope = np.array([])
    #tempEnvelope = np.array([])

    for i in range (timeCoeff,len(absAmpl),timeCoeff):
        maximum = 0
        for j in range(timeCoeff):
            maximum = max(absAmpl[i-j],maximum)
        envelope = np.append(envelope,[maximum])
    envelope = np.append(envelope,[0]) # last mesure added to fit with other data (unless lenght of envelope is missing one element)
    return envelope

def getfilteredEnvelope (envelope,intensityThreshold):
    """
    filter the amplitude envelope to the specified threshold
    
    Parameters:
    envelope,intensityThreshold
    
    Returns:
    filteredEnvelope
    """
    filteredEnvelope = np.array([])
    for i in range(len(envelope)):
        if envelope[i]>intensityThreshold:
            filteredEnvelope = np.append(filteredEnvelope, envelope[i])
        else:
            filteredEnvelope = np.append(filteredEnvelope, None)
    return filteredEnvelope

# note : faster with np.append than x[i]
def getMaxIndex (dbData,filteredEnvelope,timeCoef,lowFilter):
    """
    generate the table with the index of the max amplitude for each time indent 
    of the db data of stft transformed sound signal
    use of a filtered envelop to avoid noise data
    timeCoeff is the time indent of the envelope
    
    Parameters:
    dbData,filteredEnvelope,timeCoef,lowFilter
    
    Returns:
    maxIndex
    """

    maxIndex = np.array([])
    #dbDataToFilter = dbData # to not alter dbData
    rev_data = filterHighLowFreq(dbData,lowFilter).transpose()
    #rev_data = dbData.transpose()

    for i in range(len(dbData[1])-timeCoef-1):

            if (filteredEnvelope[i*timeCoef] == None):
                maxIndex =np.append(maxIndex,None)
            else:
                maxIndex =np.append(maxIndex, int(np.argmax(rev_data[i])))
    maxIndex = np.append(maxIndex,[None,None])

    return maxIndex

def getPitch(dbData,filteredEnvelope,timeCoef,frequencies,lowFilter):
    """
    transform the maxIndex to frequencies values. Uses getMaxIndex
    
    Parameters:
    dbData,filteredEnvelope,timeCoef,frequencies,lowFilter
    
    Returns:
    pitchValues
    """
    maxIndex = getMaxIndex (dbData,filteredEnvelope,timeCoef,lowFilter)
    pitchValues = np.array([])
    for i in range(len(maxIndex)):
        if (maxIndex[i] != None and maxIndex[i]>10):
            pitchValues = np.append(pitchValues,frequencies[int(maxIndex[i])])
        else:
            pitchValues = np.append(pitchValues,[None])
    
    return pitchValues


def filterHighLowFreq (freqData,lowFilter):
    """
    abrupt filter of high and low frequencies by setting their value to 0
    lowFilter sets the index of minimum frequencies
    High freq max are divided by 2
    freqData could be sftf signal or its db amplitude
    
    Parameters:
    freqData,lowFilter
    
    Returns:
    freqData
    """
    for i in range(lowFilter): 
        freqData[i] = 0
    for i in range(len(freqData)//2+len(freqData)//3):
        freqData[len(freqData)-1-i] = 0
    return freqData


def divideFreq(db,factor):
    """
    divides the frequencies of db amplitude of stft or db data by the integer factor
    FFT(x)=FFT_O(2x)
    heart of harmonic produc spectrum method
    transposed matrix are used to put freq data on rows, to easily access to them 
    
    Parameters:
    db,factor
    
    Returns:
    dividedData
    """
    dividedDataTransposed = np.ones((len(db),len(db[0]))).transpose()
    dbTransp = db.transpose()

    for f in range(len(db)//factor):
        for t in range (len(db[0])):
            dividedDataTransposed [t][f] = dbTransp[t][factor*f]
    dividedData = dividedDataTransposed.transpose()
    return dividedData

def harmonicProductSpectrum (db,iterations, coeff):
    """
    Makes the product of the db data with frequency divided db data (uses divideFreq) with interations number of iterations.
    A corrector factor coeff could be used to ponderate the intensity of the HPS data with initial data
    
    Parameters:
    db,iterations, coeff
    
    Returns:
    dbHPS+coeff*db
    """
    dbHPS = db
    for i in range(iterations-1):
        dbHPS = (divideFreq(db,i+2))*dbHPS
    return dbHPS+coeff*db
