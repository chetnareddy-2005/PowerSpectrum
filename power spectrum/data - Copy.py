import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from time import time
import math

start = time()

# 🔹 Change filename here
filename = r'23JU2025SHT1.r12'

fid = open(filename, 'rb')

# ---- Read header ----
A = np.fromfile(fid, dtype=np.int16, count=64)

baud = A[1]
nrgb = A[2]
nfft = A[3]     # FFT length (check this carefully)
nci = A[4]
nici = A[5]
ipp = A[6]
pw = A[7]
nbeam = A[20]
w1start = A[10]

w1len = nrgb * baud
datasize = np.uint32(nrgb) * np.uint32(nfft)
framelength = (ipp / 1000000) * nci * nfft / 3600

fid.seek(0, 0)

# ---- Count frames ----
Framecount = 0
channels = 6   # keep consistent

while True:
    _ = np.fromfile(fid, dtype=np.int16, count=64)
    _ = np.fromfile(fid, dtype=np.int32, count=channels * 2 * datasize)
    if _.size < 128:
        break
    Framecount += 1

print(f'Number of Frames: {Framecount}')
Nscan = Framecount // (nbeam * nici)
print(f'Number of Scans: {Nscan}')

# ---- Allocate arrays ----
fid.seek(0, 0)
frames = Framecount
SNR = np.zeros((channels, nrgb, frames))
rti = np.empty([nrgb, frames])

I_Data = np.zeros((channels, frames, nrgb, nfft), dtype=np.float32)
Q_Data = np.zeros((channels, frames, nrgb, nfft), dtype=np.float32)
I_raw = np.zeros((nrgb, nfft), dtype=np.float32)
Q_raw = np.zeros((nrgb, nfft), dtype=np.float32)

s = 0.00013427734375 / (nici * pw)  # Normalization
window = np.ones(nfft)

# ---- Helper functions ----
def clip_data(unclipped, high_clip, low_clip):
    np_unclipped = np.array(unclipped)
    cond_high_clip = (np_unclipped > high_clip) | (np_unclipped < low_clip)
    np_clipped = np.where(cond_high_clip, np.nan, np_unclipped)
    return np_clipped.tolist()

def ewma_fb(df_column, span):
    fwd = pd.Series.ewm(df_column, span=span).mean()
    bwd = pd.Series.ewm(df_column[::-1], span=10).mean()
    stacked_ewma = np.vstack((fwd, bwd[::-1]))
    fb_ewma = np.mean(stacked_ewma, axis=0)
    return fb_ewma

def remove_outliers(spikey, fbewma, delta):
    np_spikey = np.array(spikey)
    np_fbewma = np.array(fbewma)
    cond_delta = (np.abs(np_spikey - np_fbewma) > delta)
    np_remove_outliers = np.where(cond_delta, np.nan, np_spikey)
    return np_remove_outliers

spectra = np.zeros_like(I_Data, dtype=np.complex128)

# ---- Main loop ----
for frame in range(frames):
    for beam in range(1):
        A = np.fromfile(fid, dtype=np.int16, count=64)
        beamdate = f'{A[17]}-{A[16]}-{A[15]}.'
        beam_time = f'{A[18]}:{A[19]}:{A[20]}.'
        beamtime = np.array([A[15], A[16], A[17]])
        btime = beamtime[0] + beamtime[1] / 60 + beamtime[2] / 3600

        for i in range(channels):
            for rgb in range(nrgb):
                # 🔹 Read I/Q as int16 interleaved
                raw = np.fromfile(fid, dtype=np.int16, count=2 * nfft)

                if len(raw) < 2 * nfft:
                    print("End of file reached early")
                    break

                I_raw[rgb, :] = raw[0::2]
                Q_raw[rgb, :] = raw[1::2]

            # ---- DC Removal ----
            avg_I = np.sum(I_raw, axis=1) / nfft
            avg_Q = np.sum(Q_raw, axis=1) / nfft
            I_raw = I_raw - avg_I.reshape(-1, 1)
            Q_raw = Q_raw - avg_Q.reshape(-1, 1)
            I_raw *= s
            Q_raw *= s

            I_Data[i, frame] = I_raw
            Q_Data[i, frame] = Q_raw
            spectrum = I_Data[i, frame] + 1j * Q_Data[i, frame]
            spectrum = np.fft.fft(spectrum)
            spectrum[:, 0] = 0
            spectrum = np.fft.fftshift(spectrum, axes=1)
            spectrum = spectrum / (np.max(np.abs(spectrum)) + math.e)
            m = np.mean(spectrum)
            spectrum -= m
            spectra[i, frame] = spectrum

print("Time taken: " + str(time() - start))

# ---- Frequency axis ----
fs = 10**6 / (np.float64(ipp) * np.float64(nci))
frequency = np.linspace(-fs / 2, fs / 2, nfft)

# ---- Plotting ----
plt.figure()
plt.gca().set_facecolor('#000000')
offset = 0.2
for r in range(nrgb):   # ✅ fixed loop
    plt.plot(frequency, np.abs(spectra[2, 20, r]) + offset * r, color='green')
plt.show()
