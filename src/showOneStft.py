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
print(sampleRate)
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
index = 0
if(False):
    for i in range(645,670,5):
        plt.plot(frequencies,(abs(stftData).transpose()[i]+index)/max(abs(stftData).transpose()[i]), label = i)
with open('freq.txt', 'w') as filehandle:
    for listitem in frequencies:
        filehandle.write('%s\n' % listitem)
plt.plot(frequencies,abs(stftData).transpose()[300]/abs(stftData).transpose()[300][439])
#plt.plot(frequencies,(abs(stftData).transpose()[646]+0.2)/max(abs(stftData).transpose()[646]))
#plt.plot(frequencies,(abs(stftData).transpose()[647]+0.3)/max(abs(stftData).transpose()[647]))
#plt.plot(frequencies,(abs(stftData).transpose()[648]+0.4)/max(abs(stftData).transpose()[648]))
#plt.plot(frequencies,dbDataInit.transpose()[300]-39.6)
plt.xscale('log')
#plt.yscale('log')
plt.show()