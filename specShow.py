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

"""
Use this program to plot the spectrogram of a wav file. Pick manually the frequencies of notes to use them in extractPitch
"""

####################### Variables definitions #######################

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
####################
# envelope filtering
####################
frequencies = librosa.fft_frequencies(sr=sampleRate, n_fft=num_fft)


stftData = librosa.stft(amplitude,n_fft=num_fft) # par defaut intervalle de temps de 2048 itérations soit 93ms

dbDataInit = librosa.amplitude_to_db(abs(stftData))

"""
Put True to see the spectrogram only on short range
"""
if (False):
    LOW_FILTER_FREQUENCY = 523
    HIGH_FILTER_FREQUENCY = 585
    lowFilterIndex = functions.freqToIndex(frequencies,LOW_FILTER_FREQUENCY)
    highFilterIndex = functions.freqToIndex(frequencies,HIGH_FILTER_FREQUENCY)
    dbDataInit = functions.filterHighLowFreq(dbDataInit,lowFilterIndex,highFilterIndex)


####################### Main #######################


#plot equal temperament frequencies for precised tonic

#tonic = 256 #lousie le gall
#tonic = 990 #nedelec
#tonic = 295 # lea
tonic = 505
degrees = [tonic, tonic*(9/8),tonic*(5/4),tonic*(4/3),tonic*(3/2),tonic*(5/3),tonic*(7/4),tonic*2]
for i in range(len(degrees)):
    plt.plot(stftTime/(num_fft//2048),degrees[i]*np.ones(len(envelope)),'k')

for i in [-1,1,3,6,8,11]:
    plt.plot(stftTime/(num_fft//2048),tonic*2**(i/12)*np.ones(len(envelope)),'k--')

librosa.display.specshow(dbDataInit, sr=sampleRate, x_axis='time', y_axis='hz')

print("total duration : ",time.time() - start_time)

plt.show()