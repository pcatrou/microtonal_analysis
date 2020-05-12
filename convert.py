#from os import path
from pydub import AudioSegment

# files       
file_name = "05416"
extension = ".mp3"                                                                  
src = "audio_data/to_convert/"+file_name+extension
dst = "audio_data/"+file_name+".wav"

# convert wav to mp3                                                            
sound = AudioSegment.from_file(src)
sound.export(dst, format="wav")