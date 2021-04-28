import time
start_time = time.time()
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from numpy.core.numeric import True_
from scipy.fftpack import fft
from scipy.io import wavfile
from matplotlib import pyplot as plt
import Consts as Consts
import audio_all_methods as functions
print("total duration : ",time.time() - start_time)
# imports duration : 2s

"""
Use this program to plot the spectrogram of a wav file. Pick manually the frequencies of notes to use them in extractPitch
"""

####################### Variables definitions #######################
getEnvelope = False
isCutted = False
isHistRec = True
file_name = "2018-fil-lorient-quillay-lothode-trophee-matilin-an-dall-12-aout"
file_name = "27 Laridé"
#file_name = "Echelle biniou big"
files_path = "src/audio_data/"

tonic = Consts.TONIC_LOTHODE_QUILLAY
displayDegrees = False

if isCutted:
    file_name = file_name + "-cut"
    files_path = files_path + "cutted/"
audioData = files_path + file_name + ".wav"
if isHistRec:
    audioData = files_path + "hist_rec/" + file_name + ".wav"

amplitude,sampleRate = librosa.load(audioData,sr=None)

#nombre de points pris pour chaque FFT
num_fft = 2**15 #du à l'overlap, il y a 4 fois + de fft faites (1 fft sur 2048px mais la fenetre se deplace de 512 px)
fftNumber = num_fft//4
#Si on veut changer les steps de l'envelope, ici calqué sur fft mais peut changer + tard
if(getEnvelope):
    envelopeTimeSteps = fftNumber
    envelope = functions.getEnvelope(amplitude,envelopeTimeSteps)
    endTime = len(amplitude)/sampleRate
    audioFileTime = np.linspace(0,endTime,len(amplitude))
    stftTime = np.linspace(0,endTime,1+len(audioFileTime)//fftNumber)
    envelopeTime = \
        np.linspace(envelopeTimeSteps/sampleRate,endTime+envelopeTimeSteps/sampleRate,len(audioFileTime)//envelopeTimeSteps)
####################
# envelope filtering
####################
frequencies = librosa.fft_frequencies(sr=sampleRate, n_fft=num_fft)

stftData = librosa.stft(amplitude,n_fft=num_fft) # par defaut intervalle de temps de 2048 itérations soit 93ms

dbDataInit = librosa.amplitude_to_db(abs(stftData))
# sets max value to 0 for better visualization
dbDataInit = dbDataInit - np.max(dbDataInit)

filterSpectrum = False
if (filterSpectrum):
    for j in range(len(dbDataInit)):
        for i in range(len(dbDataInit[j])):
            if (dbDataInit[j][i]<Consts.THRESHOLD_VALUE_FOR_FILTERING):
                dbDataInit[j][i] = -29

"""
Put True to see the spectrogram only on short range
"""
displayOnShortRange = False
if (displayOnShortRange):
    LOW_FILTER_FREQUENCY = 523
    HIGH_FILTER_FREQUENCY = 585
    lowFilterIndex = functions.freqToIndex(frequencies,LOW_FILTER_FREQUENCY)
    highFilterIndex = functions.freqToIndex(frequencies,HIGH_FILTER_FREQUENCY)
    dbDataInit = functions.filterHighLowFreq(dbDataInit,lowFilterIndex,highFilterIndex)


####################### Main #######################


#plot equal temperament frequencies for precised tonic

if (displayDegrees):
    degrees = [tonic, tonic*(9/8),tonic*(5/4),tonic*(4/3),tonic*(3/2),tonic*(5/3),tonic*(7/4),tonic*2]

    for i in range(len(degrees)):
        plt.plot(stftTime/(num_fft//2048),degrees[i]*np.ones(len(envelope)),'k')

    for i in [-1,1,3,6,8,11]:
        plt.plot(stftTime/(num_fft//2048),tonic*2**(i/12)*np.ones(len(envelope)),'k--')

fig = librosa.display.specshow(dbDataInit, sr=sampleRate, x_axis='s', y_axis='log')
plt.colorbar(fig,format="%+2.f dB")


plt.show()