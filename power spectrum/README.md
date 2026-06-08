# PowerSpectrum: Radar Signal Analysis & Visualization System

A comprehensive radar signal processing and visualization platform with three integrated modules for spectral analysis, FFT visualization, and results dashboarding.

---

## 📋 Project Overview

PowerSpectrum processes raw radar data files to extract detectability metrics, visualizes frequency-domain characteristics, and displays multi-beam radar analysis results through an intuitive web interface.

### Three Core Modules:

| Module | Purpose | Input | Output |
|--------|---------|-------|--------|
| **Spectral Data Viewer** ⚙️ | Radar signal analysis engine | `.d1`, `.d2`, `.r12` radar files | Spectral metrics, detectability values |
| **FFT Plotter** 📈 | Interactive FFT visualization | I/Q signal samples | Frequency spectrum graph |
| **Radar Graph Viewer** 📊 | Web-based results dashboard | Reference + Test radar files | E-W, N-S, Detectability graphs |

---

## 🏗️ Architecture

```
Raw Radar Data
       ↓
Spectral Data Viewer (Analysis Engine)
       ├─ File Parsing
       ├─ FFT Processing
       ├─ Spectral Moments
       ├─ Detectability Calculation
       └─ SNR Computation
       ↓
Spectral Metrics
       ↓
Radar Graph Viewer (Dashboard)
       ├─ Flask Backend
       ├─ Template Rendering
       └─ Graph Display
       ↓
Web Visualization
```

**FFT Plotter** (Standalone Utility):
```
I/Q Samples → FFT Plotter (React) → Flask API → Frequency Spectrum
```

---

## 📁 Project Structure

```
PowerSpectrum/
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
├── app.py                            # Flask backend server ⭐
│
├── Core Analysis Modules:
├── spectral_data_detectability.py    # Main processing engine
├── moments.py                        # Spectral moments calculation
├── data.py                           # Data loading utilities
├── rawdata.py                        # Raw radar file parsing
│
├── Web Frontend (Radar Graph Viewer):
├── templates/
│   └── index.html                   # Dashboard UI with star background
├── uploads/                         # Uploaded radar files storage
│
├── FFT Plotter (React App):
├── fft-plotter/
│   ├── src/
│   │   ├── App.js                  # FFT visualization component
│   │   ├── App.css                 # Styling
│   │   └── index.js                # React entry point
│   ├── public/
│   │   └── index.html              # React HTML template
│   └── package.json                # NPM dependencies
│
├── Data Files (Reference):
├── 6JL2019SHT1Incoh.d2             # Reference radar data
├── 9JL2025SHT1.d11                 # Test radar data
├── detectability_ref.csv           # Pre-computed detectability metrics
├── snr_list_ref.csv                # SNR values
├── ew_ref.csv                      # E-W reference values
├── ns_ref.csv                      # N-S reference values
└── tot_power_list_ref.csv          # Total power metrics
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js & npm (for FFT Plotter)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/chetnareddy-2005/PowerSpectrum.git
cd PowerSpectrum
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install FFT Plotter dependencies (optional)**
```bash
cd fft-plotter
npm install
cd ..
```

---

## 📊 Module Guide

### 1️⃣ Spectral Data Viewer ⚙️ (Analysis Engine)

**Purpose:** Process raw radar files and extract signal characteristics.

**Key Files:**
- `spectral_data_detectability.py` - Main processing logic
- `moments.py` - Spectral moment calculations
- `rawdata.py` - Binary radar file parsing

**How It Works:**
```
1. Read binary radar file (.d1, .d2, .r12)
2. Extract header: baud rate, FFT size, beam count
3. Parse raw I/Q data
4. Apply FFT to each range bin
5. Calculate spectral moments
6. Compute detectability metrics
7. Calculate SNR per beam
```

**Key Functions:**

| Function | Purpose |
|----------|---------|
| `process_files(ref_file, test_file)` | Main processing pipeline |
| `Moments.compute()` | Calculate spectral moments |
| `parseRadarFile()` | Extract data from binary file |

**Usage (via Flask API):**
```python
from spectral_data_detectability import process_files

# Process reference and test files
graphs = process_files("6JL2019SHT1Incoh.d2", "9JL2025SHT1.d11")
```

**Output:** Matplotlib figures for E-W, N-S, and Detectability

---

### 2️⃣ FFT Plotter 📈 (DSP Visualization Tool)

**Purpose:** Interactive frequency-domain visualization of I/Q samples.

**Key Files:**
- `fft-plotter/src/App.js` - React component
- `app.py:/process` - Backend FFT computation

**How It Works:**
```
1. User enters I samples (real component)
2. User enters Q samples (imaginary component)
3. Click "Plot Graph"
4. Frontend sends to Flask /process API
5. Backend computes: signal = I + 1j*Q
6. FFT computed: fft_result = np.fft.fft(signal)
7. Magnitude spectrum returned
8. Plotly renders frequency graph
```

**Example:**
```
Input:
  I = 1, 2, 3, 4
  Q = 3, 4, 5, 6

Processing:
  signal = [1+3j, 2+4j, 3+5j, 4+6j]
  fft_result = FFT(signal)
  magnitude = |fft_result|

Output:
  Frequency spectrum graph
```

**Running FFT Plotter:**

```bash
# Terminal 1: Start Flask server
cd PowerSpectrum
python app.py
# Server runs on http://127.0.0.1:5000

# Terminal 2: Start React dev server
cd fft-plotter
npm start
# App opens on http://localhost:3000
```

**API Endpoint:**
```
POST /process
Content-Type: application/json

{
  "I": [1, 2, 3, 4],
  "Q": [3, 4, 5, 6]
}

Response:
{
  "x": [frequency_axis_values],
  "y": [magnitude_values]
}
```

---

### 3️⃣ Radar Graph Viewer 📊 (Results Dashboard)

**Purpose:** Web-based visualization of radar analysis results.

**Key Files:**
- `templates/index.html` - Dashboard UI with star background
- `app.py` - Flask routes
- CSV files - Reference metrics

**Features:**
- 🌟 Animated star background
- 📁 Drag-and-drop file upload
- 🎯 Multi-beam radar processing
- 📈 Interactive graph tabs
- ⚡ Real-time analysis

**How It Works:**
```
1. User uploads Reference File + Test File
2. Server processes files (spectral_data_detectability.py)
3. Generates 3 graphs:
   - Graph 0: E-W Reference vs Test
   - Graph 1: N-S Reference vs Test
   - Graph 2: Detectability Metrics
4. Display in tabbed interface
```

**Running Radar Graph Viewer:**

```bash
python app.py
# Open browser to http://127.0.0.1:5000
```

**Upload UI:**
```
┌─────────────────────────────────────┐
│       Upload Radar Files            │
├──────────────┬──────────────────────┤
│ Reference    │ Test                 │
│ File: [ ]    │ File: [ ] (Required) │
│ Skip: 0      │ Skip: 0              │
│ Analyze: 1   │ Analyze: 1           │
└──────────────┴──────────────────────┘
     [Upload & Process]

Generated Graphs:
[Graph 1] [Graph 2] [Graph 3]
```

---

## 🔧 Installation & Setup

### Step 1: Clone & Setup Environment

```bash
git clone https://github.com/chetnareddy-2005/PowerSpectrum.git
cd PowerSpectrum
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt contents:**
```
Flask==3.0.0
flask-cors==4.0.0
matplotlib==3.8.0
numpy>=1.24.0
```

### Step 3: Verify Test Data

Ensure these sample files exist:
- `6JL2019SHT1Incoh.d2` (Reference)
- `9JL2025SHT1.d11` (Test data)

---

## 🎯 Running Each Module

### Option A: Radar Graph Viewer Only
```bash
python app.py
# Navigate to http://127.0.0.1:5000
# Upload radar files to process and visualize
```

### Option B: FFT Plotter Only
```bash
# Terminal 1
python app.py

# Terminal 2
cd fft-plotter
npm start
```

### Option C: All Features
```bash
# Terminal 1: Backend
python app.py

# Terminal 2: FFT Plotter Frontend
cd fft-plotter
npm start

# Terminal 3: Optional - Direct Python processing
python -c "from spectral_data_detectability import process_files; process_files('6JL2019SHT1Incoh.d2', '9JL2025SHT1.d11')"
```

---

## 📊 Data Flow

### Radar File Format
```
Binary Structure:
├─ Header (64 int16 values)
│  ├─ baud (A[1])
│  ├─ nrgb (A[2])
│  ├─ nfft (A[3])
│  ├─ nci (A[4])
│  ├─ ipp (A[6])
│  └─ nbeam (A[20])
└─ Data (nrgb × nfft × int32 values)
```

### Processing Pipeline
```
Raw File → Parse Header → Extract I/Q Data → FFT → Spectral Analysis → Detectability → Visualization
```

### Output Metrics
- **E-W Reference:** East-West directional spectrum
- **N-S Reference:** North-South directional spectrum
- **Detectability:** Signal detection probability
- **SNR:** Signal-to-Noise Ratio per beam
- **Total Power:** Integrated power across frequency

---

## 🎨 UI Features

### Star Background Animation
- 150 animated stars with random colors (white, purple, blue)
- Twinkling animation (2-5s duration)
- Non-intrusive pointer events (clicks pass through)
- Dark theme for radar visualization

### Interactive Elements
- Form inputs with validation
- Tabbed graph viewer
- Real-time cache busting
- CORS-enabled API

---

## 🧪 Example: Processing Radar Files

```python
from spectral_data_detectability import process_files
import matplotlib.pyplot as plt

# Process files
graphs = process_files(
    ref_file="6JL2019SHT1Incoh.d2",
    test_file="9JL2025SHT1.d11"
)

# Returns dictionary of matplotlib figures:
# graphs[0] = E-W Analysis
# graphs[1] = N-S Analysis  
# graphs[2] = Detectability
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.0.0 | Web server |
| flask-cors | 4.0.0 | Cross-origin requests |
| numpy | ≥1.24.0 | FFT & array operations |
| matplotlib | 3.8.0 | Graph generation |
| React | 19.1.1 | FFT plotter UI |
| react-plotly.js | 2.6.0 | Interactive charts |

---

## 🏆 Key Algorithms

### 1. Spectral Moments
Calculates mean frequency, bandwidth, and higher-order statistics from power spectrum.

### 2. FFT Processing
- Applies Fast Fourier Transform to I/Q samples
- Normalizes by maximum magnitude
- Removes DC offset
- Performs FFT shift for centered frequency axis

### 3. Detectability Calculation
- Estimates SNR using spectral moments
- Applies detection threshold
- Computes probability of detection
- Beam-wise aggregation

---

## 🐛 Troubleshooting

### "File not found" error
```
Ensure sample radar files exist in project root:
- 6JL2019SHT1Incoh.d2
- 9JL2025SHT1.d11
```

### FFT Plotter blank page
```
1. Verify Flask backend running: python app.py
2. Check browser console for errors
3. Ensure ports not in use (5000, 3000)
```

### CORS errors
```
CORS is enabled in app.py. If still issues:
- Clear browser cache
- Try incognito/private mode
- Check firewall settings
```

---

## 📝 Interview Explanation

**Short Version (1 minute):**
> PowerSpectrum is a radar signal analysis platform with three modules: (1) a spectral analysis engine that processes raw radar files using FFT and computes detectability metrics, (2) an FFT plotter for visualizing frequency-domain I/Q samples, and (3) a web dashboard displaying multi-beam radar results with interactive graph visualization.

**Technical Version (2-3 minutes):**
> The system reads binary radar files containing I/Q samples organized by range bins and beams. The analysis engine extracts radar parameters from the file header (FFT size, beam count, sampling rate) and processes raw data through FFT to generate spectral analysis. We compute spectral moments to estimate signal characteristics and SNR for detectability metrics. The Flask backend exposes both file processing and FFT computation endpoints. The frontend is built with Flask templates for the main dashboard and React for the FFT plotter, providing interactive visualization with Plotly graphs. CORS enables cross-origin requests between React frontend and Flask API.

---

## 📚 Technologies Used

- **Backend:** Python, Flask, NumPy, Matplotlib
- **Frontend:** HTML/CSS, React, Plotly.js
- **Data Processing:** FFT, Spectral Analysis
- **Architecture:** RESTful API with CORS support

---

## 🔗 Links

- **Repository:** https://github.com/chetnareddy-2005/PowerSpectrum
- **Issues:** Report bugs on GitHub Issues

---

## 📄 License

This project is part of radar signal analysis research.

---

**Last Updated:** June 2026  
**Contributors:** Radar Signal Processing Team
