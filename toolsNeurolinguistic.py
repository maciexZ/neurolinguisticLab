import pandas as pd
import io
import speech_recognition as sr
import os
# Google Cloud library
from google.cloud import speech_v1
from google.cloud.speech_v1 import types,enums
from google.oauth2 import service_account

# api key from google cloud
credentials = service_account.Credentials.from_service_account_file(
    '')
client = speech_v1.SpeechClient(credentials=credentials)


############ 1 ###########
### looking for audio files in directory
def pathToAudio(PATH, extension='wav'):
    """
     searching for audiofiles in PATH directory
    :param PATH: path to directory
    :param extension: audiofile etension, wav or flac
    :return: list of strings - paths to audiofiles
    """
    audiopaths = []
    for path, directories, files in os.walk(PATH):
        for file in files:
            if f'.{extension}' in file.lower():
                audiopaths.append(os.path.join(path, file))
    return audiopaths
#end pathToAudio


########### 2 ##############
### actual speech to text

#Free option, uses python library connected to free api
#not as precise as paid google cloud option
def read_WAV(audiopath, language='en-US'):
    """
    wav to text. Free but less accurate.
    :param audiopath: path to wav file
    :param language: language of wav audio
    :return: string wth text from audio
    """
    reader = sr.Recognizer()
    WAV = sr.AudioFile(audiopath)
    with WAV as source:
        reader.adjust_for_ambient_noise(source)
        audio = reader.record(source)
        try:
            wavToText = reader.recognize_google(audio, language='{}'.format(language))
            # WAV_recorded2 = reader.recognize_google(audio, show_all=True)
        except sr.UnknownValueError as e:
            wavToText = 'NIEROZPOZNANE'
        # except sr.HTTPError as p:
        #     WAV_recorded = reader.recognize_google(audio, language=f'{language}')
        except sr.RequestError as d:
            wavToText = 'NIEROZPOZNANE'
    return wavToText
# end read_WAV



### sending to google cloud with credentials
### paid option, better accuracy
def readAudioCloud(audiopath, language='en-USA', extension='wav', chanels=1):
    """
    sending to google cloud
    :param audiopath: string path to audiofile
    :param language: language - param for google api
    :param extension: wav or flac
    :param chanels: integer (flac mostly 1 (mono) wav 2 or more)
    :return: response object from google cloud
    """
    with io.open(audiopath, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)
        config = types.RecognitionConfig(
        encoding =  enums.RecognitionConfig.AudioEncoding.FLAC if extension == 'flac'else
        enums.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=f'{language}',
        enable_word_time_offsets=True,
        audio_channel_count=chanels)
        response = client.recognize(config, audio)
    return response
#end readAudioCloud_


##############3 ###############
###human readable form of answer

def singleWordWithTime(response, audiopath, finalResults):
    """
    adjusting response object to a human readable form
    :param response: google speech-to-text object
    :param audiopath: audiopath to the said audiofile
    :param finalResults: dataFrame with results
            [FILENAME;WORD;START_TIME;END_TIME]
    """
    for result in response.results:
        print(result)
        alternative= result.alternatives[0]
        print(alternative)
        for word_info in alternative.words:
            word = word_info.word.lower()
            start_time = word_info.start_time
            end_time = word_info.end_time
            print(word + ' START {} || STOP {}'.format(start_time.seconds + start_time.nanos * 1e-9, end_time))
            finalResults.loc[len(finalResults.index) + 1] = [audiopath[audiopath.rfind('/') + 1:],
                                                             word, start_time.seconds + start_time.nanos * 1e-9, end_time.seconds + end_time.nanos * 1e-9]
# end singleWordWithTime

##############4 ###############
###checking if nothing is missing
def missingList(dataframe, audiopaths):
    """
    helping tool comparing results from google with the
    list of files sent to cloud
    :param dataframe: dataframe with results
    :param audiopaths: list with paths to audio files sent
    :return: list with missing, e.g. not recognized audiofiles
    """
    whatGoogleHeared = [filename for filename in dataframe['FILENAME']]
    audiopaths = [audiopath[audiopath.rfind('/') + 1:] for audiopath in audiopaths]
    return [filename for filename in audiopaths if filename not in whatGoogleHeared]
#end missing


def missingDataFrame(dataframe, audiopaths):
    """
    adding information about missing files to datafram with the results
    :param dataframe: dataframe with results
    :param audiopaths: list with paths to audio files sent
    :return: dataframe with results with appended missing filenames
    """
    whatGoogleHeared = [filename for filename in dataframe['FILENAME']]
    audiopathsStriped = [audiopath[audiopath.rfind('/') + 1:] for audiopath in audiopaths]
    missingAudio = [filename for filename in audiopathsStriped if filename not in whatGoogleHeared]
    for filename in missingAudio:
        dataframe.loc[len(dataframe.index)+1] = [filename,'BRAK_ODSŁUCHU','-','-']
#end missing
