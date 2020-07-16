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

####################### Variables definitions #######################

#file_name = "test-lea"
file_name = "a77547" #+"-cut"
file_name = "Gram-5080-_Biniou" +"-cut"
#file_name = "kervaRabe" +"-cut"
#file_name = "henaffMeunier-cut"
file_name = "01 Marches"
#file_name = "Echelle biniou big"
#file_name = "biniou Kerne"

#file_name = "lhn_yt-cut"
#file_name = "2015-11-09-20_02_57"
#file_name = "lebotCosquer-cut"
#file_name = "20809-cut"
#file_name = "20350-cut"
#file_name = "05416"+"-cut"
#file_name = "a77547"+"-cut"
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

#plt.plot(audioFileTime,amplitude)
#plt.plot(envelopeTime,envelope)
#plt.show()

stftData = librosa.stft(amplitude,n_fft=num_fft) # par defaut intervalle de temps de 2048 itérations soit 93ms

dbDataInit = librosa.amplitude_to_db(abs(stftData))

# Harmonic Product Spectrum method

#iterationNumbrHPS = 3
#HPSCorrectorCoeff = 20
iterationNumbrHPS = 2
HPSCorrectorCoeff = 20
dbData = functions.harmonicProductSpectrum(dbDataInit,iterationNumbrHPS,HPSCorrectorCoeff) 
amplitudeThreshold = 0.1
filteredEnvelope = functions.getfilteredEnvelope(envelope,amplitudeThreshold)
frequencies = librosa.fft_frequencies(sr=sampleRate, n_fft=num_fft)

frequenciesIntegerValues = librosa.fft_frequencies(sr=sampleRate, n_fft=num_fft)

lowFilter = functions.freqToIndex(frequenciesIntegerValues,660)

highFilter = functions.freqToIndex(frequenciesIntegerValues,715)

####################### Main #######################
pitchLine = functions.getPitch(dbDataInit,filteredEnvelope,fftNumber//envelopeTimeSteps,frequencies,lowFilter,highFilter)
average = np.array([])
for i in range(len(pitchLine)):
    if pitchLine[i] != None :
        average = np.append(average,pitchLine[i])
print(np.mean(average))
plt.plot(stftTime/(num_fft//2048),pitchLine,'g',ms=2)

#plot equal temperament frequencies for precised tonic

#tonic = 256 #lousie le gall
#tonic = 990 #nedelec
#tonic = 295 # lea
tonic = 951*2
"""
# Tonic
plt.plot(stftTime/(num_fft//2048),tonic*np.ones(len(pitchLine)),'k')
#II
plt.plot(stftTime/(num_fft//2048),tonic*(9/8)*np.ones(len(pitchLine)),'k')
#III
plt.plot(stftTime/(num_fft//2048),tonic*(5/4)*np.ones(len(pitchLine)),'k')
#IV
plt.plot(stftTime/(num_fft//2048),tonic*(4/3)*np.ones(len(pitchLine)),'k')
#V
plt.plot(stftTime/(num_fft//2048),tonic*(3/2)*np.ones(len(pitchLine)),'k')
#V
plt.plot(stftTime/(num_fft//2048),tonic*(3/2)*np.ones(len(pitchLine)),'k')
#VI
plt.plot(stftTime/(num_fft//2048),tonic*(5/3)*np.ones(len(pitchLine)),'k')
#VII harmonic
plt.plot(stftTime/(num_fft//2048),tonic*(7/4)*np.ones(len(pitchLine)),'k')

for i in [-1,1,3,6,8,11]:
    plt.plot(stftTime/(num_fft//2048),tonic*2**(i/12)*np.ones(len(pitchLine)),'k')
    #plt.plot(stftTime/(num_fft//2048),tonic*2**(-i/12)*np.ones(len(pitchLine)))
"""
#librosa.display.specshow(dbDataInit, sr=sampleRate, x_axis='time', y_axis='hz')

print("total duration : ",time.time() - start_time)

plt.show()