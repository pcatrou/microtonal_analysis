from pydub import AudioSegment

isHistRec = False
files_path = "src/audio_data/"

file_name = "2018-fil-lorient-quillay-lothode-trophee-matilin-an-dall-12-aout"
extension = ".mp3"

startMin = 0
startSec = 9

endMin = 1
endSec = 30

def convertAudioToWav(src,dst):
    """
    convert audio file to wav and saves it to audio_data folder
    """
    srcFile = files_path + "to_convert/" + src
    dstFile = files_path + dst

    if isHistRec:
        srcFile = files_path + "to_convert/hist_rec/" + src
        dstFile = files_path + "hist_rec/" + dst
    sound = AudioSegment.from_file(srcFile)
    sound.export(dstFile, format= "wav")

def cutAudio (startMin,startSec,endMin,endSec):
    """
    cut the wav audio file and saves it to audio_data folder
    adds a -cut to the file name
    """
    startTime = startMin*60*1000+startSec*1000
    endTime = endMin*60*1000+endSec*1000
    path = files_path
    if isHistRec :
        path = files_path +"hist_rec/"
    song = AudioSegment.from_mp3( path + file_name + '.wav' )
    extract = song[startTime:endTime]
    if isHistRec :
        extract.export(files_path + "cutted/hist_rec/" + file_name + '-cut.wav', format="wav")
    else :
        extract.export(files_path + "cutted/" + file_name + '-cut.wav', format="wav")

src = file_name + extension
dst = file_name + ".wav"

if extension != ".wav":
    convertAudioToWav(src, dst)

cutAudio (startMin, startSec, endMin, endSec)
# Time to miliseconds
