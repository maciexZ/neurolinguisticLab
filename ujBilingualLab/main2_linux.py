import pandas as pd
import io
import speech_recognition as sr
import os
# Imports the Google Cloud client library
from google.cloud import speech, speech_v1
import google.cloud.speech_v1
from google.cloud.speech_v1 import types,enums
from google.oauth2 import service_account

# ręcznie podajemy klucz api, żeby móc skorzystać z usług chmury
credentials = service_account.Credentials.from_service_account_file(
    '')
client = speech_v1.SpeechClient(credentials=credentials)

# Spisuje pliki WAV z podanych folderów do tabeli
def read_WAV(PATH, language='en-US'):
    df = pd.DataFrame([], columns=['NAZWA PLIKU', 'ODSŁUCH'])
    reader = sr.Recognizer()
    for path, directories, files in os.walk(PATH):
        for file in files:
            if '.wav' in file.lower():
                WAV = file
                WAV2 = sr.AudioFile(os.path.join(path,file))
                with WAV2 as source:
                    reader.adjust_for_ambient_noise(source)
                    audio = reader.record(source)
                    try:
                        WAV_recorded = reader.recognize_google(audio, language=f'{language}')
                        # WAV_recorded2 = reader.recognize_google(audio, show_all=True)
                    except sr.UnknownValueError as e:
                        WAV_recorded = 'NIEROZPOZNANE'
                    # except sr.HTTPError as p:
                    #     WAV_recorded = reader.recognize_google(audio, language=f'{language}')
                    except sr.RequestError as d:
                        WAV_recorded = 'NIEROZPOZNANE'
                df.loc[len(df.index)+1] = [WAV,WAV_recorded]
                os.chdir(PATH)
                df.to_excel(f'agaWynik_{language}.xlsx')
# end read_WAV

# Spisuje pliki WAV z podanych folderów do tabeli z wykorzystaniem chmury google (podaje czasówki)
#Krótkie pliki
def read_WAV_cloud(PATH,language='en-USA'):
    df = pd.DataFrame([], columns=['NAZWA PLIKU', 'SŁOWO','CZAS START', 'KONIEC SLOWA'])
    for path, directories, files in os.walk(PATH):
        for file in files:
            if '.wav' in file.lower():
                WAV = file
                #odczytuje wszystkie pliki wav w folderze wskazanym (także te z folderów w folderze)
                with io.open(os.path.join(path,file), 'rb') as audio_file:
                    content = audio_file.read()
                    audio = types.RecognitionAudio(content=content)
                    config = types.RecognitionConfig(
                        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                        language_code=f'{language}',
                        enable_word_time_offsets=True)
                    # ustawienia naszego odczytywania audio
                    response = client.recognize(config, audio)
                    # odczyt
                    for response in response.results:
                        alternative= response.alternatives[0]
                        print(alternative)
                        # ta zmienna zawiera sczytaną całą wypowiedz
                        for word_info in alternative.words:
                            # iteracja słowo po słowie
                            word = word_info.word
                            start_time = word_info.start_time
                            end_time = word_info.end_time
                            print(word + ' START {} || STOP {}'.format(start_time.seconds + start_time.nanos * 1e-9, end_time))
                            df.loc[len(df.index) + 1] = [WAV, word, start_time.seconds + start_time.nanos * 1e-9, end_time.seconds + end_time.nanos * 1e-9]
                            os.chdir(PATH)
                            df.to_excel(f'badanie_{language}.xlsx')
# end red_WAV_cloud






