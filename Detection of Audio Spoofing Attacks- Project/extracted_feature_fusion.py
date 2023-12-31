# -*- coding: utf-8 -*-
"""Extracted_Feature_fusion.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14SDy1OBmUkPwh7jC7QueQINLCMLfOu7u
"""

import numpy as np
import pandas as pd
import librosa
import csv
import os
import pandas as pd
import numpy as np

import seaborn as sn
import matplotlib.pyplot as plt
#matplotlib inline
!pip install mpld3
import mpld3
mpld3.enable_notebook()

from sklearn.decomposition import PCA
from sklearn.utils import shuffle
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier
import sklearn.metrics as mt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import recall_score, precision_score, accuracy_score
from sklearn.metrics import confusion_matrix, f1_score, classification_report
from sklearn.model_selection import cross_val_score

#Feature Extraction
#Here,we are extacting the following features:

#rms
#spectral_centroid
#spectral_bandwidth
#spectral rolloff
#zero_crossing_rate
#MFCCs (13)
#Chroma Features(12)
header = 'filename rms spectral_centroid spectral_bandwidth rolloff zero_crossing_rate '
for i in range(0, 13):
    header += f' mfcc_{i}'
    
for i in range(0,12 ):
    header += f' chroma_feature{i}'
    
header += ' label'
header = header.split()

file = open('Extracted_Features.csv', 'w', newline='')
with file:
    writer = csv.writer(file)
    writer.writerow(header)

signals = 'Bonafide Spoofed'.split()
for i in signals:
    for filename in os.listdir(f'/content/drive/MyDrive/ASVSpoof-2021 Dataset/PA/{i}'):
        audioname = f'/content/drive/MyDrive/ASVSpoof-2021 Dataset/PA/{i}/{filename}'
        y, sr = librosa.load(audioname)
        rms = librosa.feature.rms(y=y)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        mfcc = librosa.feature.mfcc(y=y,n_mfcc=13, sr=sr)
        chromagram = librosa.feature.chroma_stft(y,sr=sr,hop_length=512)
        to_append = f'{filename} {np.mean(rms)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'    
        for e in mfcc:
            to_append += f' {np.mean(e)}'
        for e in chromagram:
            to_append += f' {np.mean(e)}'
        to_append += f' {i}'
        file = open('Extracted_Features.csv', 'a', newline='')
        with file:
            writer = csv.writer(file)
            writer.writerow(to_append.split())

df=pd.read_csv("Extracted_Features.csv", on_bad_lines='skip')