from pydub import AudioSegment

def convertAudioToWav(src,dst):

    sound = AudioSegment.from_file(src)
    sound.export(dst, format="wav")

def cutAudio (startMin,startSec,endMin,endSec):
    startTime = startMin*60*1000+startSec*1000
    endTime = endMin*60*1000+endSec*1000

    song = AudioSegment.from_mp3( files_path+file_name+'.wav' )
    extract = song[startTime:endTime]

    extract.export(files_path+ file_name+'-cut.wav', format="wav")

file_name = "20350"
extension = ".mp3"
src = "audio_data/to_convert/"+file_name+extension
dst = "audio_data/"+file_name+".wav"

if extension != ".wav":
    convertAudioToWav(src,dst)

files_path = 'audio_data/'

startMin = 0
startSec = 3

endMin = 0
endSec = 30

cutAudio (startMin,startSec,endMin,endSec)
# Time to miliseconds
