import time
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile
from matplotlib import pyplot as plt

import audio_all_methods as functions
import Consts as Consts
# imports duration : 11s

start_time = time.time()

#######################
# Variables definitions
#######################
file_name = "2018-fil-lorient-quillay-lothode-trophee-matilin-an-dall-12-aout"
isCutted = False
isHistRec = False
writeToNoteDeviations = False

isCutted = False
isHistRec = True
#file_name = "2018-fil-lorient-quillay-lothode-trophee-matilin-an-dall-12-aout"
file_name = "27 Laridé"
files_path = "src/audio_data/"
tonic = Consts.TONIC_LARIDE_1932
frequenciesBound = Consts.FREQ_BOUND_LARIDE_MAGADUR

noteHalfTone = [-1,0,2,4,5,7,9,10,11]

files_path = "src/audio_data/"
audioData = "src/audio_data/"+file_name+".wav"
if isCutted:
    file_name = file_name + "-cut"
    files_path = files_path + "cutted/"
audioData = files_path + file_name + ".wav"
if isHistRec:
    audioData = files_path + "hist_rec/" + file_name + ".wav"


#frequenciesBound = frequenciesBound * (tonic // Consts.TONIC_MARCHES)

showSpecOnShortRange = False
showPitchLines = False
removeIrrelevantDataForIII = False
isMinorSecondPresent = False

amplitude,sampleRate = librosa.load(audioData, sr= None)

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
envelopeTime = \
    np.linspace(envelopeTimeSteps/sampleRate,endTime+envelopeTimeSteps/sampleRate,len(audioFileTime)//envelopeTimeSteps)

stftData = librosa.stft(amplitude,n_fft=num_fft) # par defaut intervalle de temps de 2048 itérations soit 93ms

dbDataInit = librosa.amplitude_to_db(abs(stftData))
# normalisation
dbDataInit = (dbDataInit/np.max(dbDataInit)) - np.max(dbDataInit)

##################################
# Harmonic Product Spectrum method
##################################
useHPS = False
if useHPS:
    iterationNumbrHPS = 2
    HPSCorrectorCoeff = 20
    dbData = functions.harmonicProductSpectrum(dbDataInit,iterationNumbrHPS,HPSCorrectorCoeff) 

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
        pitchLine = \
            functions.getPitch(librosa.amplitude_to_db(abs(stftData)),\
                filteredEnvelope,fftNumber//envelopeTimeSteps,frequencies,lowFilterIndex,highFilterIndex)
        pitchLines.append(pitchLine)
    return pitchLines


pitchLines = getAllPitchLines(frequenciesBound)

if (removeIrrelevantDataForIII):
    ### Correction for III (noise values)
    degree = 4
    for i in range (len(pitchLines[degree])):
        if pitchLines[degree][i] != None and pitchLines[degree][i] > 645:
            pitchLines[degree][i] = None

# set to None values for minor second because it is irrelevant

if isMinorSecondPresent:
    for i in range(len(pitchLines[2])):
        pitchLines[2][i]=None

noteValues = functions.getAllNotesVariations(pitchLines)

averageNoteValue = []
noteDeviationInCents=[]

#noteHalfTone = [-1,0,None,2,4,5,None,7,9,10,11]
halfTonesFinal = []
for i in range(len(noteValues)):
    if sum(noteValues[i]) and noteHalfTone[i] != None:
        averageNoteValue.append(sum(noteValues[i])/len(noteValues[i]))
        noteDeviationInCents.append(1200*np.log2(averageNoteValue[-1]/tonic) - 100*noteHalfTone[i])
        halfTonesFinal.append(noteHalfTone[i])
if(writeToNoteDeviations):
    with open('noteDeviations/'+ file_name +'.txt', 'w') as filehandle:
        for listitem in noteDeviationInCents:
            filehandle.write('%s\n' % listitem)
    with open('noteDeviations/'+ file_name +'half-tones' +'.txt', 'w') as filehandle:
        for listitem in halfTonesFinal:
            filehandle.write('%s\n' % listitem)
    
#############
# plot 
#############

fig, (ax1, ax2) = plt.subplots(1, 2)
frameSize = len(noteValues[1])

degrees = [tonic, tonic*(9/8),tonic*(5/4),tonic*(4/3),tonic*(3/2),tonic*(5/3),tonic*(7/4),tonic*2]
# plots the tones lines
for i in range(len(degrees)):
    ax1.semilogy(degrees[i]*np.ones(frameSize),'k')

# plot the half tones lines
for i in [-1,1,3,6,8,11]:
    ax1.semilogy(tonic*2**(i/12)*np.ones(frameSize),'k--')

#plots the pitch data
for i in range(len(noteValues)):
    if i != 6:
        ax1.semilogy(noteValues[i],'o', ms =2)

print("total duration : ",time.time() - start_time)

# plots the average values for each degree
ax2.plot(halfTonesFinal,noteDeviationInCents,'o')
ax2.plot(halfTonesFinal,np.zeros(len(halfTonesFinal)),'k')
ax2.grid(True)
ax1.set_title('variation de hauteur des notes au cours du temps')
ax1.set(xlabel="numéro d'occurence de la note",ylabel='fréquence (Hz)')
ax2.set(xlabel="demi-ton d'écart à la tonique", ylabel='déviation au tempérament égal (cents)')
ax2.set_title('écart de hauteur des degrés par rapport au tempérament égal')

plt.show()


###
# plot figures to show validity of the method
###

if(showPitchLines): # Used to check where the notes are
    for i in range(len(pitchLines)):
        plt.plot(pitchLines[i],'k')

"""
Put True to see the spectrogram only on short range
"""

if (showSpecOnShortRange):
    plt.plot(stftTime/(num_fft//2048),pitchLines[5],'k')
    LOW_FILTER_FREQUENCY = 661
    HIGH_FILTER_FREQUENCY = 728
    lowFilterIndex = functions.freqToIndex(frequencies,LOW_FILTER_FREQUENCY)
    highFilterIndex = functions.freqToIndex(frequencies,HIGH_FILTER_FREQUENCY)
    dbDataInit = functions.filterHighLowFreq(dbDataInit,lowFilterIndex,highFilterIndex)
    librosa.display.specshow(dbDataInit, sr=sampleRate, x_axis='time', y_axis='hz',fmin=661,fmax=728)
    #plt.specgram(dbDataInit)
    scale_factor = 4
    plt.show()



# xmin, xmax = plt.xlim()
# plt.xlim(xmin * scale_factor, xmax * scale_factor)


