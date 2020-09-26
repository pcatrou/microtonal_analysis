import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile
from matplotlib import pyplot as plt

import audio_all_methods as functions
# imports duration : 11s
import time
start_time = time.time()

#######################
# Variables definitions
#######################

#file_name = "test-lea"
file_name = "a77547" #+"-cut"
file_name = "Gram-5080-_Biniou" +"-cut"
#file_name = "kervaRabe" +"-cut"
#file_name = "henaffMeunier-cut"
file_name = "01 Marches-cut"
#file_name = "Echelle biniou big"
#file_name = "biniou Kerne"

#file_name = "lhn_yt-cut"
#file_name = "2015-11-09-20_02_57"
#file_name = "lebotCosquer-cut"
#file_name = "20809-cut"
#file_name = "20350-cut"
#file_name = "05416"+"-cut"
#file_name = "a77547"+"-cut"

#audioData = "audio_data/"+file_name+".wav"
audioData = "audio_data/hist_rec/"+file_name+".wav"
amplitude,sampleRate = librosa.load(audioData)

#########################
# audio signal processing
#########################

#nombre de points pris pour chaque FFT
num_fft = 2**14 #du à l'overlap, il y a 4 fois + de fft faites (1 fft sur 2048px mais la fenetre se deplace de 512 px)
fftNumber = num_fft//4
#Si on veut changer les steps de l'envelope, ici calqué sur fft mais peut changer + tard
envelopeTimeSteps = fftNumber
envelope = functions.getEnvelope(amplitude,envelopeTimeSteps)

endTime = len(amplitude)/sampleRate
audioFileTime = np.linspace(0,endTime,len(amplitude))
stftTime = np.linspace(0,endTime,1+len(audioFileTime)//fftNumber)
envelopeTime = np.linspace(envelopeTimeSteps/sampleRate,endTime+envelopeTimeSteps/sampleRate,len(audioFileTime)//envelopeTimeSteps)

stftData = librosa.stft(amplitude,n_fft=num_fft) # par defaut intervalle de temps de 2048 itérations soit 93ms

dbDataInit = librosa.amplitude_to_db(abs(stftData))

##################################
# Harmonic Product Spectrum method
##################################

"""
iterationNumbrHPS = 2
HPSCorrectorCoeff = 20
dbData = functions.harmonicProductSpectrum(dbDataInit,iterationNumbrHPS,HPSCorrectorCoeff) 
"""

####################
# envelope filtering
####################

amplitudeThreshold = 0.1
filteredEnvelope = functions.getfilteredEnvelope(envelope,amplitudeThreshold)
frequencies = librosa.fft_frequencies(sr=sampleRate, n_fft=num_fft)

####################################################
# Main 
####################################################
def getAllPitchLines(frequenciesBound):
    """
    This method gets all the notes pithcLine into all the frequencies frame given in frequenciesBound.
    Parameters:
    frequenciesBound
    
    Returns:
    pitchLines (list of pitchLine)
    """
    pitchLines = []
    for i in range(len(frequenciesBound)-1):
        LOW_FILTER_FREQUENCY = frequenciesBound[i]
        HIGH_FILTER_FREQUENCY = frequenciesBound[i+1]
        lowFilterIndex = functions.freqToIndex(frequencies,LOW_FILTER_FREQUENCY)
        highFilterIndex = functions.freqToIndex(frequencies,HIGH_FILTER_FREQUENCY)
        pitchLine = functions.getPitch(librosa.amplitude_to_db(abs(stftData)),filteredEnvelope,fftNumber//envelopeTimeSteps,frequencies,lowFilterIndex,highFilterIndex)
        pitchLines.append(pitchLine)
    return pitchLines

frequenciesBound = [461,485,523,585,661,728,758,804,855,905,975]
pitchLines = getAllPitchLines(frequenciesBound)

noteValues = functions.getAllNotesVariations(pitchLines)

tonic = 505
averageNoteValue = []
noteDeviationInCents=[]
noteHalfTone = [-1,0,2,4,5,7,7,9,10,11]
for i in range(len(noteValues)):
    if (sum(noteValues[i])):
        averageNoteValue.append(sum(noteValues[i])/len(noteValues[i]))
        noteDeviationInCents.append(1200*np.log2(averageNoteValue[-1]/tonic) - 100*noteHalfTone[i])

#############
# plot 
#############
frameSize = len(noteValues[1])

degrees = [tonic, tonic*(9/8),tonic*(5/4),tonic*(4/3),tonic*(3/2),tonic*(5/3),tonic*(7/4),tonic*2]

for i in range(len(degrees)):
    plt.plot(degrees[i]*np.ones(frameSize),'k')

for i in [-1,1,3,6,8,11]:
    plt.plot(tonic*2**(i/12)*np.ones(frameSize),'k--')

for i in range(len(noteValues)):
    plt.plot(noteValues[i])

print("total duration : ",time.time() - start_time)

plt.show()

plt.plot(noteDeviationInCents,'o')
plt.plot(np.zeros(len(noteDeviationInCents)),'k')
plt.show()

