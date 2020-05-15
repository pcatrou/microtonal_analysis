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

file_name = "test-lea"
#file_name = "20809-cut"
#file_name = "20350-cut"
#file_name = "05416"+"-cut"
#file_name = "a77547"+"-cut"
audioData = "audio_data/"+file_name+".wav"
amplitude,sampleRate = librosa.load(audioData)

#nombre de points pris pour chaque FFT
num_fft = 2**13
#du à l'overlap, il y a 4 fois + de fft faites (1 fft sur 2048px mais la fenetre se deplace de 512 px)
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

# Harmonic Product Spectrum method

#dbData2 = functions.divideFreq(dbDataInit,2)
#dbData3 = functions.divideFreq(dbDataInit,3)
#dbData = dbDataInit*dbData2*dbData3+20*dbDataInit+10*dbData2
iterationNumbrHPS = 3
HPSCorrectorCoeff = 20
dbData = functions.harmonicProductSpectrum(dbDataInit,iterationNumbrHPS,HPSCorrectorCoeff) 
amplitudeThreshold = 0.03
filteredEnvelope = functions.getfilteredEnvelope(envelope,amplitudeThreshold)
frequencies = librosa.fft_frequencies(sr=sampleRate, n_fft=num_fft)
lowFilter = 40

####################### Main #######################
pitchLine = functions.getPitch(dbData,filteredEnvelope,fftNumber//envelopeTimeSteps,frequencies,lowFilter)

plt.plot(stftTime/(num_fft//2048),pitchLine,'black')

#plot equal temperament frequencies for precised tonic
''' tonic = 233
plt.plot(stftTime/(num_fft//2048),tonique*np.ones(len(pitchLine)))
plt.plot(stftTime/(num_fft//2048),tonique*2**(2/12)*np.ones(len(pitchLine)))
plt.plot(stftTime/(num_fft//2048),tonique*2**(3/12)*np.ones(len(pitchLine)))
plt.plot(stftTime/(num_fft//2048),tonique*2**(5/12)*np.ones(len(pitchLine)))
plt.plot(stftTime/(num_fft//2048),tonique*2**(-2/12)*np.ones(len(pitchLine)))
plt.plot(stftTime/(num_fft//2048),tonique*2**(-3/12)*np.ones(len(pitchLine)))
plt.plot(stftTime/(num_fft//2048),tonique*2**(-5/12)*np.ones(len(pitchLine)))
plt.plot(stftTime/(num_fft//2048),tonique*2**(-7/12)*np.ones(len(pitchLine))) '''

librosa.display.specshow(dbDataInit, sr=sampleRate, x_axis='time', y_axis='log')
print("total duration : ",time.time() - start_time)

plt.show()