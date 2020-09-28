from pydub import AudioSegment

def convertAudioToWav(src,dst):

    sound = AudioSegment.from_file(src)
    sound.export(dst, format="wav")

def cutAudio (startMin,startSec,endMin,endSec):
    startTime = startMin*60*1000+startSec*1000
    endTime = endMin*60*1000+endSec*1000

    song = AudioSegment.from_mp3( files_path+file_name+'.wav' )
    extract = song[startTime:endTime]

    extract.export(files_path+ file_name+'-2.wav', format="wav")

# file_name = "Echelle biniou big"
# file_name = "Biniou Kerne"
# extension = ".mov"

file_name = "01 Marches"
extension = ".m4a"
#file_name = "2015-11-09-20_02_57"
#extension = ".wav"
src = "audio_data/to_convert/hist_rec/"+file_name+extension
dst = "audio_data/hist_rec/"+file_name+".wav"

if extension != ".wav":
    convertAudioToWav(src,dst)

files_path = 'audio_data/hist_rec/'

startMin = 0
startSec = 2

endMin = 3
endSec = 11

cutAudio (startMin,startSec,endMin,endSec)
# Time to miliseconds
