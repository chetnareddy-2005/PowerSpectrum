# 🚀 PowerSpectrum – Radar Signal Processing & Spectral Analysis System

## 📌 Overview

PowerSpectrum is a Radar Signal Processing and Spectral Analysis application designed to process raw radar signal data, perform spectral analysis, compute detectability metrics, and visualize radar beam characteristics through an interactive web interface.

The system combines a Python Flask backend for radar data processing with React-based visualization modules for FFT and signal analysis.

---

## 🎯 Features

### Radar Data Processing

* Supports binary radar data formats:

  * `.d1`
  * `.d2`
  * `.r12`
* Extracts beam-wise radar information from raw signal files.
* Processes reference and test radar datasets.
* Supports multi-beam radar analysis.

---

### Signal Analysis

The application performs:

* Fast Fourier Transform (FFT) based spectral analysis
* Signal Detectability Calculation
* Signal-to-Noise Ratio (SNR) Estimation
* Total Power Computation
* Spectral Moment Analysis
* Directional Velocity Analysis

---

### Multi-Beam Radar Analysis

The system analyzes five radar beams simultaneously:

1. East Beam
2. West Beam
3. Zenith Beam
4. North Beam
5. South Beam

This allows comparison between reference and test radar measurements across multiple directions.

---

### Directional Metrics

The application generates:

* East-West (E-W) Spectral Metrics
* North-South (N-S) Spectral Metrics
* Detectability Profiles
* Power Distribution Analysis
* Beam-wise Performance Comparison

---

## 📊 Generated Visualizations

### Graph 1 – Directional Spectral Analysis

* E-W Reference
* N-S Reference
* E-W Test
* N-S Test

### Graph 2 – Signal Quality Metrics

* Detectability
* Signal-to-Noise Ratio (SNR)
* Total Power

### Graph 3 – Beam-wise Detectability

Comparison of:

* East Beam
* West Beam
* Zenith Beam
* North Beam
* South Beam

for both reference and test datasets.

---

## 🖥️ System Architecture

### Backend

* Python
* Flask
* NumPy
* Pandas
* Matplotlib

Responsibilities:

* Radar file parsing
* FFT processing
* Spectral calculations
* Graph generation
* Detectability analysis

---

### Frontend

#### FFT Plotter

React-based visualization tool that:

* Accepts I/Q signal samples
* Performs FFT analysis
* Displays frequency-domain plots

#### Interactive Visualization

* Plotly.js
* React
* Dynamic graph rendering
* Signal spectrum visualization

---

## 📂 Project Structure

```text
PowerSpectrum/
│
├── app.py
├── spectral_data_detectability.py
├── moments.py
├── rawdata.py
├── data.py
│
├── uploads/
├── templates/
│
├── fft-plotter/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── my-app/
│
└── data/
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/chetnareddy-2005/PowerSpectrum.git
cd PowerSpectrum
```

---

## ▶️ Run Flask Backend

```bash
pip install -r requirements.txt
python app.py
```

Server starts at:

```text
http://localhost:5000
```

---

## ▶️ Run FFT Plotter (React)

```bash
cd fft-plotter
npm install
npm start
```

Runs at:

```text
http://localhost:3000
```

---

## ▶️ Run React Application

```bash
cd my-app
npm install
npm start
```

Runs at:

```text
http://localhost:3000
```

---

## 📈 Workflow

1. Upload Reference Radar File
2. Upload Test Radar File
3. Process Raw Radar Data
4. Extract FFT Spectra
5. Compute Detectability Metrics
6. Generate Spectral Analysis Graphs
7. Visualize Results through Web Interface

---

## 💻 Tech Stack

### Backend

* Python
* Flask
* NumPy
* Pandas
* Matplotlib

### Frontend

* React
* Plotly.js
* FFT.js
* React Scripts

### Data Formats

* `.d1`
* `.d2`
* `.r12`
* `.csv`

---

## 🎓 Applications

* Radar Signal Processing
* Spectral Analysis
* Signal Detectability Studies
* Research & Development
* Atmospheric Radar Systems
* Digital Signal Processing (DSP)

---

## 👩‍💻 Author

**Chetna Reddy**

GitHub: https://github.com/chetnareddy-2005
