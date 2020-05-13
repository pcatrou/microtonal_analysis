from pydub import AudioSegment

files_path = 'audio_data/'
file_name = 'a77547'

startMin = 0
startSec = 0

endMin = 0
endSec = 10

# Time to miliseconds
startTime = startMin*60*1000+startSec*1000
endTime = endMin*60*1000+endSec*1000

# Opening file and extracting segment
song = AudioSegment.from_mp3( files_path+file_name+'.wav' )
extract = song[startTime:endTime]

# Saving
extract.export(files_path+ file_name+'-cut.wav', format="wav")