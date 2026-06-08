import time
import numpy as np
import os
import math
import plotly.graph_objects as go

start = time.time()

# === File details ===
directory = ''
filename = r'9JL2025SHT1Incoh.d11'
file_path = os.path.join(directory, filename)
file = open(file_path, 'rb')

# === Read header ===
A = np.fromfile(file, dtype=np.int16, count=64)
baud = A[1]
nrgb = A[2]
nfft = A[3]
nci = A[4]
ipp = A[6]
nbeam = A[20]
nici = 1

# === Frequency axis ===
fs = 10**6 / (np.float64(ipp) * np.float64(nci))
frequency = np.linspace(-fs / 2, fs / 2, nfft)
datasize = np.uint32(nrgb) * np.uint32(nfft)

# === Count frames ===
framecount = 0
file.seek(0, 0)
while True:
    x = np.fromfile(file, dtype=np.int16, count=64)
    x = np.fromfile(file, dtype=np.int32, count=datasize)
    if x.size < 128:
        break
    framecount += 1

print(f"Total frames: {framecount}")
file.seek(0, 0)

# === Store spectra for each frame ===
frames_data = []

for frame_idx in range(min(framecount, 10)):  # Limit to first 10 frames for speed
    file.seek((128 + 4 * datasize) * frame_idx + 128, 0)

    spectra = np.zeros((nrgb, nfft), dtype=np.float64)
    for rgb in range(nrgb):
        for ft in range(nfft):
            val = np.fromfile(file, dtype=np.int32, count=1)
            spectra[rgb, ft] = val
        spectra[rgb, :] /= (np.max(np.abs(spectra[rgb, :])) + math.e)
        spectra[rgb, :] -= np.mean(spectra[rgb, :])

    spectra = np.fft.fftshift(spectra, axes=1)
    frames_data.append(np.abs(spectra))

# === Create Plotly figure ===
fig = go.Figure()

# First frame
offset = 0.02
for rgb in range(nrgb):
    fig.add_trace(go.Scatter(
        x=frequency,
        y=frames_data[0][rgb] + offset * rgb,
        mode='lines',
        line=dict(color='lime', width=1),
        name=f"RGB {rgb}",
        showlegend=False
    ))

# Slider steps
steps = []
for i in range(len(frames_data)):
    step_data = []
    for rgb in range(nrgb):
        step_data.append(dict(
            x=frequency,
            y=frames_data[i][rgb] + offset * rgb
        ))
    step = dict(
        method="update",
        args=[{"x": [d["x"] for d in step_data],
               "y": [d["y"] for d in step_data]},
              {"title": f"Frame {i}"}],
        label=str(i)
    )
    steps.append(step)

sliders = [dict(
    active=0,
    currentvalue={"prefix": "Frame: "},
    pad={"t": 50},
    steps=steps
)]

fig.update_layout(
    title="Radar Spectrum Viewer",
    sliders=sliders,
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white"),
    xaxis_title="Frequency",
    yaxis_title="Amplitude + Offset"
)

# Save HTML
fig.write_html("spectral_slider.html")
print("✅ Saved as spectral_slider.html")

