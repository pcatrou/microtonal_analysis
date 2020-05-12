import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile
from matplotlib import pyplot as plt


#TODO mettre un if pour l'ouverture. if: .mp3 : convert into temp file. ensuite le supprimer

audioData = 'audio_data/a77547-cut.wav'

rawData,sampleRate = librosa.load(audioData) #TODO se passer de librosa
endTime = len(rawData)/sampleRate
time = np.linspace(0,endTime,len(rawData))

stftTime = np.linspace(0,endTime,1+len(time)//512)
print(len(stftTime))
""" plt.plot(time,rawData)
plt.show() """

stftData = librosa.stft(rawData)
dbData = librosa.amplitude_to_db(abs(stftData))
print(len(dbData[1]),len(stftData[12]),len(rawData))