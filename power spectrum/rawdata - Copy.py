import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from time import time
import math

start = time()

filename = r'23JU2025SHT1.r12'

fid = open(filename, 'rb')
A = np.fromfile(fid, dtype=np.int16, count=64)
    
baud = A[1]
nrgb = A[2]
nfft = A[3]
nci = A[4]
nici = A[5]
ipp = A[6]
pw = A[7]
nbeam = A[20]
w1start = A[10]
w1len = nrgb * baud
datasize = np.uint32(nrgb) * np.uint32(nfft)
framelength = (ipp/1000000)*nci*nfft/3600

fid.seek(0,0)

Framecount = 0
channels = 6

while True:
    _ = np.fromfile(fid, dtype=np.int16, count=64)
    _ = np.fromfile(fid, dtype=np.int32, count=channels*2*datasize)
    if _.size < 128:
        break
    Framecount += 1

# nici = 1
print(f'Number of Frames: {Framecount}')
Nscan = Framecount // (nbeam * nici)
print(f'Number of Scans: {Nscan}')

fid.seek(0, 0)
frames = Framecount
SNR = np.zeros((channels, nrgb, frames))
rti = np.empty([nrgb, frames])

I_Data = np.zeros((channels, frames, nrgb, nfft), dtype=np.float32) #Change to float32 for ESWAR
Q_Data = np.zeros((channels, frames, nrgb, nfft), dtype=np.float32)
I_raw = np.zeros((nrgb, nfft), dtype=np.float32) #Change to float32 for ESWAR
Q_raw = np.zeros((nrgb, nfft), dtype=np.float32)

s = 0.00013427734375/(nici*pw) #Normalization
window = np.ones(nfft)

def clip_data(unclipped, high_clip, low_clip):
    ''' Clip unclipped between high_clip and low_clip. 
    unclipped contains a single column of unclipped data.'''
    
    # convert to np.array to access the np.where method
    np_unclipped = np.array(unclipped)
    # clip data above HIGH_CLIP or below LOW_CLIP
    cond_high_clip = (np_unclipped > high_clip) | (np_unclipped < low_clip)
    np_clipped = np.where(cond_high_clip, np.nan, np_unclipped)
    return np_clipped.tolist()

def ewma_fb(df_column, span):
    ''' Apply forwards, backwards exponential weighted moving average (EWMA) to df_column. '''
    # Forwards EWMA.
    fwd = pd.Series.ewm(df_column, span=span).mean()
    # Backwards EWMA.
    bwd = pd.Series.ewm(df_column[::-1],span=10).mean()
    # Add and take the mean of the forwards and backwards EWMA.
    stacked_ewma = np.vstack(( fwd, bwd[::-1] ))
    fb_ewma = np.mean(stacked_ewma, axis=0)
    return fb_ewma

def remove_outliers(spikey, fbewma, delta):
    ''' Remove data from df_spikey that is > delta from fbewma. '''
    np_spikey = np.array(spikey)
    np_fbewma = np.array(fbewma)
    cond_delta = (np.abs(np_spikey-np_fbewma) > delta)
    np_remove_outliers = np.where(cond_delta, np.nan, np_spikey)
    return np_remove_outliers

spectra = np.zeros_like(I_Data, dtype=np.complex128)

for frame in range(frames):
    # print("Frame: ", frame+1)
    for beam in range(1):  
        A = np.fromfile(fid, dtype=np.int16, count=64)
        beamdate = f'{A[17]}-{A[16]}-{A[15]}.'
        beam_time = f'{A[18]}:{A[19]}:{A[20]}.'
        beamtime = np.array([A[15], A[16], A[17]])
        btime = beamtime[0] + beamtime[1] / 60 + beamtime[2] / 3600

        for i in range(channels):
            
            for rgb in range(nrgb):
                I_raw[rgb, :] = np.fromfile(fid, dtype=np.float32, count=nfft)
                Q_raw[rgb, :] = np.fromfile(fid, dtype=np.float32, count=nfft)
            
            # for rgb in range(nrgb):

            #DC Removal
            avg_I = np.sum(I_raw, axis=1) / nfft
            avg_Q = np.sum(Q_raw, axis=1) / nfft
            I_raw = I_raw - avg_I.reshape(-1, 1)
            Q_raw = Q_raw - avg_Q.reshape(-1, 1)
            I_raw *= s
            Q_raw *= s
            
            # idf = pd.DataFrame()
            # qdf = pd.DataFrame()

            # for rgb in range(nrgb):
            #     idf['raw'] = I_raw[rgb]
            #     qdf['raw'] = Q_raw[rgb]
            #     idf['clipped'] = clip_data(idf['raw'].tolist(), 0.3, -0.3)
            #     qdf['clipped'] = clip_data(qdf['raw'].tolist(), 0.3, -0.3)
            #     idf['ewma'] = ewma_fb(idf['clipped'], 3)
            #     qdf['ewma'] = ewma_fb(qdf['clipped'], 3)
            #     idf['remove_outliers'] = remove_outliers(idf['clipped'].tolist(), idf['ewma'].tolist(), delta=0.07)
            #     qdf['remove_outliers'] = remove_outliers(qdf['clipped'].tolist(), qdf['ewma'].tolist(), delta=0.07)
            #     # ax = idf.plot(y=['raw', 'clipped', 'ewma', 'remove_outliers'])
            #     # plt.show()
            #     I_Data[i, frame, rgb] = idf['remove_outliers'].interpolate()
            #     Q_Data[i, frame, rgb] = qdf['remove_outliers'].interpolate()

            I_Data[i, frame] = I_raw
            Q_Data[i, frame] = Q_raw
            spectrum = I_Data[i, frame] + 1j * Q_Data[i, frame]
            spectrum = np.fft.fft(spectrum)
            spectrum[:,0] = 0
            spectrum = np.fft.fftshift(spectrum, axes=1)
            spectrum = spectrum / (np.max(np.abs(spectrum)) + math.e)
            m = np.mean(spectrum)
            spectrum -= m
            spectra[i, frame] = spectrum

            fftbc = 32
            fftfact = nfft // fftbc

            #RTI
            # rgb_power = np.empty(nrgb)
            
            # for j in range(nrgb):
            #     # rgb_power[j] = np.sum(data_psmag[j,:])
            #     rgb_power[j] = np.nansum(np.power(I_Data[i, frame, j, :],2) + np.power(Q_Data[i, frame, j, :],2))
            #     rti = 10*np.log10(np.abs(rgb_power[j]))
            #     if np.isnan(rti):
            #         print('HERE')
            #     SNR[i, j, frame] = rti
            
            

            # # Calculate SNR
            # npower = np.sum((I_Data[i, frame, nrgb - 1, :] ** 2) + (Q_Data[i, frame, nrgb - 1, :] ** 2))
            # for j in range(nrgb):
            #     power = np.sum((I_Data[i, frame, j, :] ** 2) + (Q_Data[i, frame, j, :] ** 2))
            #     spower = np.abs(power - npower)
            #     snr = 10 * np.log10(spower / npower)
            #     SNR[i, j, frame] = snr

# SNR[SNR < -10] = -10
# SNR[SNR > 20] = 20

print("Time taken: " + str(time() - start))
channels=2
fs = 10**6 / (np.float64(ipp) * np.float64(nci))
frequency = np.linspace(-fs / 2, fs / 2, nfft)
# fig, ax = plt.subplots(nrows=1, ncols=channels)
# offset = 0.2
# for i in range(channels):
#     for rgb in range(nrgb):
#         ax[i].plot(frequency, np.abs(spectra[i, 20, rgb]) + offset * rgb, color='green')
# plt.show()

plt.figure()
plt.gca().set_facecolor('#000000')
offset = 0.2
for rgb in range(rgb):
    plt.plot(frequency, np.abs(spectra[2, 20, rgb]) + offset * rgb, color='green')
plt.show()

# fig, ax = plt.subplots(nrows=channels, ncols=1)
# time_grid, range_grid = np.meshgrid(range(frames), range(nrgb))
# for i in range(channels):
#     im = ax[i].pcolormesh(time_grid, range_grid, SNR[i], cmap='jet', shading='gouraud')
#     fig.colorbar(im)
# plt.show()

# df = pd.DataFrame(np.vstack((np.array([nrgb, frames,0,0,0,0]), SNR.reshape(channels, nrgb*frames).T)))
# df.to_csv("SNR_csv\\" + filename + ".csv")
# a = 0