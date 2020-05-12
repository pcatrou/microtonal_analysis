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
file_name = "05416"
#file_name = "a77547"
cutted =  "-cut"
audioData = "audio_data/"+file_name+cutted+".wav"
amplitude,sampleRate = librosa.load(audioData)

num_fft = 2**12
fftNumber = num_fft//4
delta = fftNumber
envelope = functions.getEnvelope(amplitude,delta)


endTime = len(amplitude)/sampleRate
audioFileTime = np.linspace(0,endTime,len(amplitude))
stftTime = np.linspace(0,endTime,1+len(audioFileTime)//fftNumber)
envelopeTime = np.linspace(delta/sampleRate,endTime+delta/sampleRate,len(audioFileTime)//delta)

stftData = librosa.stft(amplitude,n_fft=num_fft) # par defaut intervalle de temps de 2048 itérations soit 93ms
dbData = librosa.amplitude_to_db(abs(stftData))

filteredEnvelope = functions.getfilteredEnvelope(envelope,0.03)
frequencies = librosa.fft_frequencies(sr=sampleRate, n_fft=num_fft)

####################### Main #######################

songLine = functions.extractMainSongLineWithMaxMethod(dbData,filteredEnvelope,fftNumber//delta,frequencies)

plt.xlim(0,endTime)
plt.plot(stftTime/(num_fft//2048),songLine,'black')

librosa.display.specshow(dbData, sr=sampleRate, x_axis='time', y_axis='log')
print("total duration : ",time.time() - start_time)

plt.show()
