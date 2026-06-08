import time
import numpy as np
import matplotlib
matplotlib.use("Agg")   # for Flask non-GUI backend
import matplotlib.pyplot as plt
import os
import math
from moments import Moments
def process_files(filenameRef, filename):
    start = time.time()

    # -----------------------------
    # Reference File Processing
    # -----------------------------
    file = open(filenameRef, 'rb')
    A = np.fromfile(file, dtype=np.int16, count=64)
    print(A)

    baud = A[1]; nrgbRef = A[2]; nfft = A[3]; nci = A[4]; ipp = A[6]; nbeam = A[20]
    nici = 1
    fs = 1e6 / (np.float64(ipp) * np.float64(nci))
    frequency = np.linspace(-fs/2, fs/2, nfft)
    framelength = (ipp/1e6)*nci*nfft
    print(f"Frame length: {framelength} s")

    datasize = np.uint32(nrgbRef) * np.uint32(nfft)
    print(f'datasize: {datasize}') 
    framecount = 0
    file.seek(0,0)
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

    beams = 5
    spectra = np.zeros((beams, nrgbRef, nfft), dtype=np.float64)
    detectabilityRef = np.zeros((1, beams, nrgbRef))
    ew_ref, ns_ref = np.zeros((1, nrgbRef)), np.zeros((1, nrgbRef))
    snr_list_ref, tot_power_list_ref = [], []

    file.seek(0,0)
    for beam in range(beams):
        file.seek(128,1)
        for rgb in range(nrgbRef):
            spectra[beam, rgb, :] = np.fromfile(file=file, dtype=np.float32, count=nfft)

        noise = np.sort(spectra[beam, :, :], axis=1)[:,:230]
        nsd = np.std(noise, axis=1)
        detectabilityRef[0, beam] = np.max(spectra[beam], axis=1) / nsd
        spectra[beam] = np.fft.fftshift(spectra[beam], axes=1)
        m = Moments(spectra[beam], ipp, nci)
        _, tot_power, _, _, snr = m.compute()
        snr_list_ref.append(snr)
        tot_power_list_ref.append(tot_power)

    ew_ref[0,:] = frequency[np.argmax(spectra[0,:,:], axis=1)] + frequency[np.argmax(spectra[1,:,:], axis=1)]
    ns_ref[0,:] = frequency[np.argmax(spectra[3,:,:], axis=1)] + frequency[np.argmax(spectra[4,:,:], axis=1)]

    # -----------------------------
    # Test File Processing
    # -----------------------------
    file = open(filename, 'rb')
    A = np.fromfile(file, dtype=np.int16, count=64)
    print(A)

    baud = A[1]; nrgb = A[2]; nfft = A[3]; nci = A[4]; ipp = A[6]; nbeam = A[20]
    nici = 1
    fs = 1e6 / (np.float64(ipp) * np.float64(nci))
    frequency = np.linspace(-fs/2, fs/2, nfft)
    framelength = (ipp/1e6)*nci*nfft
    print("a")
    print(f"Frame length: {framelength} s")

    datasize = np.uint32(nrgb) * np.uint32(nfft)
    print(f'datasize: {datasize}') 
    framecount = 0
    file.seek(0,0)
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

    spectra = np.zeros((beams, nrgb, nfft), dtype=np.float64)
    detectability = np.zeros((1, beams, nrgb))
    ew, ns = np.zeros((1, nrgb)), np.zeros((1, nrgb))
    snr_list, tot_power_list = [], []

    file.seek(0,0)
    for beam in range(beams):
        file.seek(128,1)
        for rgb in range(nrgb):
            spectra[beam, rgb, :] = np.fromfile(file=file, dtype=np.float32, count=nfft)

        noise = np.sort(spectra[beam, :, :], axis=1)[:,:230]
        nsd = np.std(noise, axis=1)
        detectability[0, beam] = np.max(spectra[beam], axis=1) / nsd
        spectra[beam] = np.fft.fftshift(spectra[beam], axes=1)
        m = Moments(spectra[beam], ipp, nci)
        _, tot_power, _, _, snr = m.compute()
        snr_list.append(snr)
        tot_power_list.append(tot_power)

    ew[0,:] = frequency[np.argmax(spectra[0,:,:], axis=1)] + frequency[np.argmax(spectra[1,:,:], axis=1)]
    ns[0,:] = frequency[np.argmax(spectra[3,:,:], axis=1)] + frequency[np.argmax(spectra[4,:,:], axis=1)]

    # -----------------------------
    # Plotting
    # -----------------------------

    # Graph 1: E-W / N-S
    fig1, ax = plt.subplots(2,2, figsize=(10,8))
    ax[0,0].plot(np.mean(ew_ref,axis=0), np.arange(nrgbRef)); ax[0,0].set_title("E-W Reference")
    ax[0,1].plot(np.mean(ns_ref,axis=0), np.arange(nrgbRef)); ax[0,1].set_title("N-S Reference")
    ax[1,0].plot(np.mean(ew,axis=0), np.arange(nrgb)); ax[1,0].set_title("E-W Test")
    ax[1,1].plot(np.mean(ns,axis=0), np.arange(nrgb)); ax[1,1].set_title("N-S Test")
    fig1.tight_layout()

    # Graph 2: Detectability / SNR / Power
    fig2, ax = plt.subplots(1,3, figsize=(15,8), sharey=True)
    ax[0].plot(10*np.log10(np.mean(np.mean(detectabilityRef,axis=0),axis=0)), np.arange(nrgbRef), label="Reference")
    ax[0].plot(10*np.log10(np.mean(np.mean(detectability,axis=0),axis=0)), np.arange(nrgb), label="Test")
    ax[0].set_title("Detectability"); ax[0].legend()

    ax[1].plot(np.mean(snr_list_ref,axis=0), np.arange(nrgbRef), label="Reference")
    ax[1].plot(np.mean(snr_list,axis=0), np.arange(nrgb), label="Test")
    ax[1].set_title("SNR"); ax[1].legend()

    ax[2].plot(10*np.log10(np.mean(tot_power_list_ref,axis=0)), np.arange(nrgbRef), label="Reference")
    ax[2].plot(10*np.log10(np.mean(tot_power_list,axis=0)), np.arange(nrgb), label="Test")
    ax[2].set_title("Total Power"); ax[2].legend()
    fig2.tight_layout()

    # Graph 3: Detectability per Beam
    labels = ["East","West","Zenith","North","South"]
    fig3, ax = plt.subplots(1,beams, figsize=(20,6), sharey=True)
    for b in range(beams):
        ax[b].plot(10*np.log10(np.mean(detectabilityRef,axis=0)[b]), np.arange(nrgbRef), label="Reference")
        ax[b].plot(10*np.log10(np.mean(detectability,axis=0)[b]), np.arange(nrgb), label="Test")
        ax[b].set_title(labels[b]); ax[b].legend()
    fig3.tight_layout()

    # Save PNG copies also
    out_dir = "uploads"
    os.makedirs(out_dir, exist_ok=True)
    fig1.savefig(os.path.join(out_dir,"graph1.png"))
    fig2.savefig(os.path.join(out_dir,"graph2.png"))
    fig3.savefig(os.path.join(out_dir,"graph3.png"))

    return {0: fig1, 1: fig2, 2: fig3}