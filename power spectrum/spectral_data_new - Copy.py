import time
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import math

start = time.time()
directory = ''
filename = r'9JL2025SHT1Incoh.d11'
file_path = os.path.join(directory,filename)
file = open(file_path,'rb')

def read_radar_data(file_path):
    with open(file_path,'rb') as f:
        radar_data = f.read()
    return radar_data

header_size = 128
def read_first_128_bytes(file_path):
    with open(file_path, 'rb') as file:
        first_128 = file.read(128)
    return first_128

A = np.fromfile(file, dtype=np.int16, count=64)
print(A)

# Old Receiver
# Radartype = A[0]
baud = A[1]
nrgb = A[2]
nfft = A[3]
nci = A[4]
# masteripp = A[5]
ipp = A[6]
# pw = A[7]
nbeam = A[20]
w1start = A[10]
# w1len = nrgb * baud
nici = 1

# # New Receiver
# MagicNumber     = A[0]
# pw              = A[1]/100
# ipp             = A[2]
# baud      = A[3]/100
# nrgb            = A[4]
# nfft            = A[5]
# nci             = A[6]
# nici            = A[7]
# W1start         = A[8]/100
# W1len           = A[9]/100
# CodeFlag        = A[10]
# nbeam           = A[11]
# CrntBeam_Theta  = A[12]/100
# CrntBeam_Phi    = A[13]/100
# RadarType       = A[14]

fs = 10**6 / (np.float64(ipp) * np.float64(nci))
frequency = np.linspace(-fs / 2, fs / 2, nfft)
framelength = (ipp/1000000)*nci*nfft
print(f"Frame length: {framelength} s")

datasize = np.uint32(nrgb) * np.uint32(nfft)
print(f'datasize: {datasize}') 
Resolution_of_height = 1.5*100*baud
framecount = 0
file.seek(0,0)
print('78')
while True:
    x = np.fromfile(file, dtype=np.int16, count=64)
    x = np.fromfile(file, dtype=np.int32, count=datasize)
    framecount += 1
    if x.size < 128:
       framecount -= 1
       break

nscan = framecount // (nbeam*nici)
print(f'Number of Frames: {framecount}')
print(f'Number of scans: {nscan}')
print(f"Total duration: {framelength*framecount/60} min")

frameskip = 3

file.seek((128+4*datasize)*frameskip+128,0)

index = 0
spectra = np.zeros((nrgb, nfft), dtype=np.float64)

# for rgb in range(65,75):
#     plt.figure()
#     plt.plot(B[rgb, :])
#     plt.show()

for rgb in range(nrgb):
    for ft in range(nfft):
        spectra[rgb, ft] = np.fromfile(file=file, dtype=np.int32, count=1)
    
    spectra[rgb, :] = spectra[rgb,:] / (np.max(np.abs(spectra[rgb,:])) + math.e)
    m = np.mean(spectra[rgb, :])
    spectra[rgb, :] -= m

spectra = np.fft.fftshift(spectra, axes=1)
#print(I_Data_raw)
# I_Data[:,0] = 0 
# Q_Data[:,0] = 0
# avg_I = np.sum(I_Data, axis=1) / nfft
# avg_Q = np.sum(Q_Data, axis=1) / nfft
# I_Data = I_Data - avg_I.reshape(-1, 1)
# Q_Data = Q_Data - avg_Q.reshape(-1, 1)

plt.figure(figsize=(10, 6))
plt.gca().set_facecolor('#000000')
offset = 0.02
for rgb in range(nrgb):
    plt.plot(frequency, np.abs(spectra[rgb]) + offset * rgb, color='green')
    peak = np.argmax(spectra[rgb, :])
    # plt.scatter(frequency[peak], spectra[rgb, peak] + offset * rgb, color='red')
plt.show()