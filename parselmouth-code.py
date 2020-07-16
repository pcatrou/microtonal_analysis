import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import parselmouth as ps
#### already exiting pitch detectoir ####

#sns.set() # Use seaborn's default style to make attractive graphs
file_name = "test-lea"
#file_name = "2015-11-09-20_02_57-cut"
#file_name = "05416"
#file_name = "a77547" #+"-cut"
file_name = "drumel"
#file_name = "Gram-5080-_Biniou-cut"

audioData = "audio_data/"+file_name+".wav"
# Plot nice figures using Python's "standard" matplotlib library
snd = ps.Sound(audioData)

def draw_spectrogram(spectrogram, dynamic_range=70):
    X, Y = spectrogram.x_grid(), spectrogram.y_grid()
    sg_db = 10 * np.log10(spectrogram.values)
    plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() - dynamic_range, cmap='afmhot')
    plt.ylim([spectrogram.ymin, spectrogram.ymax])
    plt.xlabel("time [s]")
    plt.ylabel("frequency [Hz]")

def draw_intensity(intensity):
    plt.plot(intensity.xs(), intensity.values.T, linewidth=3, color='w')
    plt.plot(intensity.xs(), intensity.values.T, linewidth=1)
    plt.grid(False)
    plt.ylim(0)
    plt.ylabel("intensity [dB]")

intensity = snd.to_intensity()
spectrogram = snd.to_spectrogram()


def draw_pitch(pitch):
    # Extract selected pitch contour, and
    # replace unvoiced samples by NaN to not plot
    pitch_values = pitch.selected_array['frequency']
    pitch_values[pitch_values==0] = np.nan
    plt.plot(pitch.xs(), pitch_values,color='black')
    #plt.plot(pitch.xs(), pitch_values, 'o', markersize=1)
    #plt.grid(False)
    #plt.ylim(0, pitch.ceiling)
    #plt.ylabel("fundamental frequency [Hz]")
'''
pitch = snd.to_pitch()
# If desired, pre-emphasize the sound fragment before calculating the spectrogram
pre_emphasized_snd = snd.copy()
pre_emphasized_snd.pre_emphasize()
spectrogram = pre_emphasized_snd.to_spectrogram(window_length=0.03, maximum_frequency=8000)
plt.figure()
#draw_spectrogram(spectrogram)
plt.twinx()
draw_pitch(pitch)
plt.xlim([snd.xmin, snd.xmax])
plt.show() # or plt.savefig("spectrogram_0.03.pdf")
'''
pitch = snd.to_pitch()
# If desired, pre-emphasize the sound fragment before calculating the spectrogram
#pre_emphasized_snd = snd.copy()
#pre_emphasized_snd.pre_emphasize()
#spectrogram = pre_emphasized_snd.to_spectrogram(window_length=0.03, maximum_frequency=8000)
#plt.figure()
#draw_spectrogram(spectrogram)
#plt.twinx()
draw_pitch(pitch)
plt.xlim([snd.xmin, snd.xmax])

tonic = 242 #lousie le gall
tonic = 181 #drumel
#tonic = 295 # lea
plt.plot(tonic*np.ones(len(pitch.xs())))
plt.plot(tonic*2**(8/12)*np.ones(len(pitch.xs())))
for i in [2,3,4,5,7]:
    plt.plot(tonic*2**(i/12)*np.ones(len(pitch.xs())))
    plt.plot(tonic*2**(-i/12)*np.ones(len(pitch.xs())))

plt.show() # or plt.savefig("spectrogram_0.03.pdf")