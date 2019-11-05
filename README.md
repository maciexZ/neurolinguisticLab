# neurolinguisticLab
Staff I make to help them work. 

Google speech-to-text to help processing a raw data from experiments.

Example of usage: 
A data set from an expriment: picture naming. 

For the convenience of the reserchers, script runs in a docker on the server. The users only need to upload the files via Nextcloud. 
Systemd path and systemd service are checking the upload directory and run the script whenever .wav files are detected. 

Importing, preparing container for the results
```
from toolsNeurolinguistic import pathToAudio, readAudioCloud, singleWordWithTime, missingDataFrame
import os
import pandas as pd

dataFrameResults = pd.DataFrame(columns=['FILENAME','WORD','TIME_START','TIME_STOP'])
errors = ''
pathToRawData = ''
```

A list of paths to wav files
```
audiopaths = pathToAudio(pathToRawData)
```
Actual speech-to-text processing.
```
for audiopath in audiopaths:
    try:
        response = readAudioCloud(audiopath, language='pl-PL',chanels=2)
        singleWordWithTime(response,audiopath,dataFrameResults)
        dataFrameResults.to_excel('badanie.xlsx')
    except Exception as e:
        print(e)
        errors += '\n{} - {}'.format(audiopath,e)
```
Checking for the unconverted audio files and errors
```
missingDataFrame(dataFrameResults,audiopaths)
dataFrameResults.to_excel('badanie.xlsx')

if errors != '':
    with open('errors.txt', 'w') as file:
        file.write(errors)
```
