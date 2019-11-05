from main2 import read_WAV_cloud
import os
from shutil import move

#path to .WAV files
path = r''


pathPL = r''
pathENG = r''

# rozdzielanie raw wav wg języka
for path, directories, files in os.walk(path):
    for file in files:
        if '.wav' in file.lower():
            if file[-8] != '1' and file[-8] != '2':
                move(path + '\\' + file, pathENG)
            else:
                move(path + '\\' + file, pathPL)

# sczytywanie english
# read_WAV_cloud(r'')
# #
# # #sczytywanie polish
# read_WAV_cloud(r'')
