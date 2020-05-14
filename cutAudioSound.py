from pydub import AudioSegment

files_path = 'audio_data/'
file_name = '05416'

startMin = 0
startSec = 3

endMin = 0
endSec = 30

# Time to miliseconds
startTime = startMin*60*1000+startSec*1000
endTime = endMin*60*1000+endSec*1000

# Opening file and extracting segment
song = AudioSegment.from_mp3( files_path+file_name+'.wav' )
extract = song[startTime:endTime]

# Saving
extract.export(files_path+ file_name+'-cut.wav', format="wav")