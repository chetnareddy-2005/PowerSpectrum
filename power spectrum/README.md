# 🚀 PowerSpectrum – Radar Signal Processing & Spectral Analysis System

## 📌 Overview

PowerSpectrum is a comprehensive **Radar Signal Processing and Spectral Analysis application** designed to process raw radar signal data, perform spectral analysis, compute detectability metrics, and visualize radar beam characteristics through an interactive web interface.

The system combines a **Python Flask backend** for radar data processing with **React-based visualization modules** for FFT analysis and signal visualization.

---

## 🎯 Three Core Modules

PowerSpectrum consists of three integrated modules working together:

| Module | Purpose | Input | Output | Technology |
|--------|---------|-------|--------|-----------|
| **⚙️ Spectral Data Viewer** | Radar analysis engine | `.d1`, `.d2`, `.r12` radar files | Spectral metrics, detectability graphs | Python, NumPy, FFT |
| **📈 FFT Plotter** | I/Q frequency visualization | I/Q signal samples | Frequency spectrum graph | React, Plotly.js |
| **📊 Radar Graph Viewer** | Web-based results dashboard | Reference + Test radar files | E-W, N-S, Detectability graphs | Flask, HTML/CSS, Matplotlib |

---

## 🏗️ How They Work Together

```
Raw Radar Data (.d1, .d2, .r12)
        ↓
[1] Spectral Data Viewer ⚙️
    - Parse binary radar file
    - Extract header parameters
    - Apply FFT to each range bin
    - Calculate spectral moments
    - Compute detectability metrics
    - Generate matplotlib figures
        ↓
    Spectral Analysis Results
        ↓
[3] Radar Graph Viewer 📊
    - Display results in web dashboard
    - Interactive graph tabs
    - Real-time visualization
```

**[2] FFT Plotter** (Standalone Utility):
```
I/Q Signal Samples
    ↓
User enters I, Q values
    ↓
[FFT Plotter] 📈
- Frontend: React input form
- Backend: /process API endpoint
- Computation: np.fft.fft()
    ↓
Frequency Spectrum Graph
```

---

## 🎯 Key Features

### Radar Data Processing
✅ Supports binary radar formats: `.d1`, `.d2`, `.r12`  
✅ Extracts beam-wise radar information  
✅ Processes reference and test datasets  
✅ Multi-beam (5 beams) radar analysis  

### Signal Analysis
✅ **FFT-based spectral analysis**  
✅ **Detectability calculation**  
✅ **SNR (Signal-to-Noise Ratio) estimation**  
✅ **Total power computation**  
✅ **Spectral moment analysis**  

### Multi-Beam Radar Analysis
Analyzes five radar beams simultaneously:
1. **East Beam**
2. **West Beam**
3. **Zenith Beam**
4. **North Beam**
5. **South Beam**

### Generated Visualizations
- **Graph 1:** E-W & N-S Reference vs Test Spectra
- **Graph 2:** Detectability Profiles & SNR Metrics
- **Graph 3:** Beam-wise Detectability Comparison

---

## 📂 Project Structure

```
PowerSpectrum/
│
├── README.md                          ← You are here
├── ARCHITECTURE.md                    ← Technical deep-dive
├── requirements.txt                   ← Python dependencies
│
├── Core Processing (Python):
├── app.py                            ⭐ Flask backend server
├── spectral_data_detectability.py    ⭐ Main analysis engine
├── moments.py                        → Spectral moments calculation
├── data.py                           → Data loading utilities
├── rawdata.py                        → Binary file parsing
│
├── Web Frontend (Radar Dashboard):
├── templates/
│   └── index.html                   ⭐ Dashboard with star background
├── uploads/                         → Uploaded radar files
│
├── FFT Plotter (React App):
├── fft-plotter/
│   ├── src/
│   │   ├── App.js                  ⭐ FFT visualization
│   │   ├── App.css
│   │   └── index.js
│   └── package.json
│
├── Reference Data:
├── 6JL2019SHT1Incoh.d2             → Sample reference radar file
├── 9JL2025SHT1.d11                 → Sample test radar file
├── detectability_ref.csv           → Pre-computed metrics
├── snr_list_ref.csv                → SNR values
├── ew_ref.csv, ns_ref.csv          → Directional data
└── tot_power_list_ref.csv          → Power metrics
```

---

## ⚙️ Installation & Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/chetnareddy-2005/PowerSpectrum.git
cd PowerSpectrum
```

### Step 2: Create Python Environment

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac
```

### Step 3: Install Python Dependencies

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

### Step 4: Verify Sample Data

Ensure these files exist in project root:
- ✅ `6JL2019SHT1Incoh.d2` (Reference data)
- ✅ `9JL2025SHT1.d11` (Test data)

---

## ▶️ Running the Application

### Option A: Radar Graph Viewer Only (Recommended First)

```bash
python app.py
```

Then open browser:
```
http://127.0.0.1:5000
```

**Features:**
- Upload reference + test radar files
- Click "Upload & Process"
- View 3 graphs in tabs
- Star background animation

---

### Option B: FFT Plotter + Backend

**Terminal 1 - Start Flask Backend:**
```bash
python app.py
```

**Terminal 2 - Start React FFT Plotter:**
```bash
cd fft-plotter
npm install
npm start
```

Then open:
```
http://localhost:3000
```

**Usage:**
1. Enter I values (e.g., `1,2,3,4`)
2. Enter Q values (e.g., `3,4,5,6`)
3. Click "Plot Graph"
4. See frequency spectrum

---

### Option C: All Modules (Full Stack)

**Terminal 1 - Backend:**
```bash
python app.py
```

**Terminal 2 - FFT Plotter React:**
```bash
cd fft-plotter
npm install
npm start
```

**Terminal 3 - Optional Direct Processing:**
```bash
python -c "from spectral_data_detectability import process_files; process_files('6JL2019SHT1Incoh.d2', '9JL2025SHT1.d11')"
```

---

## 📊 Module Details

### ⚙️ Module 1: Spectral Data Viewer (Analysis Engine)

**Files:**
- `spectral_data_detectability.py` - Main processing pipeline
- `moments.py` - Spectral moment calculations
- `rawdata.py` - Binary radar file parsing

**Processing Flow:**
```python
1. Read binary radar file header
   ├─ Extract: baud rate, FFT size, beam count
   ├─ Calculate: sampling frequency = 1e6 / (ipp × nci)
   └─ Determine: frequency axis

2. Parse raw I/Q data for each range bin

3. Apply FFT to each range bin

4. Calculate spectral characteristics
   ├─ Moments (mean freq, bandwidth)
   ├─ Power spectrum
   └─ Detectability metrics

5. Generate matplotlib figures
   └─ E-W, N-S, Detectability graphs
```

**Example Usage:**
```python
from spectral_data_detectability import process_files

graphs = process_files(
    ref_file="6JL2019SHT1Incoh.d2",
    test_file="9JL2025SHT1.d11"
)
# Returns: {0: fig_ew, 1: fig_ns, 2: fig_detectability}
```

---

### 📈 Module 2: FFT Plotter (DSP Visualization)

**Files:**
- `fft-plotter/src/App.js` - React component
- `app.py:/process` - Backend FFT API

**How it Works:**
```
Input:
  I = [1, 2, 3, 4]
  Q = [3, 4, 5, 6]
  
Processing:
  signal = I + 1j×Q = [1+3j, 2+4j, 3+5j, 4+6j]
  fft = numpy.fft.fft(signal)
  magnitude = |fft|
  frequency = numpy.fft.fftfreq(len(signal))
  
Output:
  Plotly graph with frequency (x) vs magnitude (y)
```

**API Endpoint:**
```
POST http://127.0.0.1:5000/process
Content-Type: application/json

Request:
{
  "I": [1, 2, 3, 4],
  "Q": [3, 4, 5, 6]
}

Response:
{
  "x": [...frequency values...],
  "y": [...magnitude values...]
}
```

---

### 📊 Module 3: Radar Graph Viewer (Web Dashboard)

**Files:**
- `templates/index.html` - Dashboard UI with star animation
- `app.py` - Flask routes
- CSV files - Reference metrics

**Features:**
- 🌟 **Animated star background** (150 stars, twinkling)
- 📁 **Drag-and-drop file upload**
- 📈 **Interactive tabbed graphs**
- ⚡ **Real-time processing**

**Workflow:**
```
1. User uploads Reference File + Test File
2. Server processes via spectral_data_detectability.py
3. Generates 3 matplotlib figures
4. Display in tabbed interface with cache-busting
```

---

## 💻 Technology Stack

### Backend
- **Python 3.8+**
- **Flask 3.0.0** - Web server
- **NumPy** - FFT computations & array operations
- **Matplotlib** - Graph generation
- **flask-cors** - Cross-origin requests

### Frontend
- **HTML/CSS** - Dashboard UI
- **React 19.1.1** - FFT plotter interface
- **Plotly.js** - Interactive graphs
- **JavaScript** - Star animation

### Data Formats
- `.d1` - Radar data format
- `.d2` - Radar data format
- `.r12` - Radar data format
- `.csv` - Reference metrics

---

## 📈 Data Processing Flow

### Binary Radar File Format

```
File Structure:
├─ Header (128 bytes = 64 × int16)
│  ├─ A[1]:  BAUD (baud rate)
│  ├─ A[2]:  NRGB (range bins)
│  ├─ A[3]:  NFFT (FFT size)
│  ├─ A[4]:  NCI (coherent integrations)
│  ├─ A[6]:  IPP (inter-pulse period, µs)
│  └─ A[20]: NBEAM (number of beams)
│
├─ Frame 1 Data
│  └─ NRGB × NFFT × int32 values
├─ Frame 2 Data
│  └─ ...
└─ Frame N Data
```

### Processing Pipeline

```
Raw File
  ↓
[1] Parse Header → Extract parameters
  ↓
[2] Read Raw Data → I/Q samples for each range bin
  ↓
[3] Apply FFT → Frequency domain conversion
  ↓
[4] Normalize → Remove DC offset, scale magnitude
  ↓
[5] Calculate Moments → Mean frequency, bandwidth
  ↓
[6] Compute Detectability → SNR, detection probability
  ↓
[7] Generate Graphs → Matplotlib figures
  ↓
Results (E-W, N-S, Detectability)
```

---

## 🎓 Applications

✅ Radar signal processing  
✅ Spectral analysis & visualization  
✅ Signal detectability studies  
✅ Research & development  
✅ Atmospheric radar systems  
✅ Digital signal processing (DSP)  
✅ Educational demonstrations  

---

## 🔍 Common Use Cases

### Use Case 1: Compare Radar Measurements
```
1. Upload reference radar file (baseline)
2. Upload test radar file (new measurement)
3. System automatically generates comparison graphs
4. Analyze differences in E-W, N-S, and detectability
```

### Use Case 2: Visualize Frequency Spectrum
```
1. Go to FFT Plotter at http://localhost:3000
2. Enter I/Q signal samples
3. Click "Plot Graph"
4. Instant frequency spectrum visualization
```

### Use Case 3: Educational Learning
```
1. Understand FFT concepts with FFT Plotter
2. Learn about radar signal processing
3. Explore spectral analysis with real data
```

---

## 📝 Interview Explanation

### Quick Pitch (1 minute):
> PowerSpectrum is a radar signal analysis platform with three modules: a Python-based analysis engine processing raw radar files using FFT and computing detectability metrics, an interactive FFT plotter for frequency-domain I/Q visualization, and a web-based dashboard displaying multi-beam radar results with an animated starry background.

### Technical Explanation (2-3 minutes):
> The system reads binary radar files containing I/Q samples organized by range bins and beams. The analysis engine extracts radar parameters from the file header and processes data through FFT to generate spectral analysis. We compute spectral moments to estimate signal characteristics and SNR for detectability. The Flask backend exposes both file processing and FFT endpoints. The frontend uses Flask templates for the dashboard and React for the FFT plotter, with Plotly providing interactive visualization. CORS enables seamless cross-origin communication.

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **"File not found" error** | Ensure `6JL2019SHT1Incoh.d2` and `9JL2025SHT1.d11` exist in project root |
| **FFT Plotter blank page** | Verify Flask running on 5000, React on 3000. Check browser console |
| **CORS errors** | Clear browser cache, try incognito mode, verify firewall |
| **"Module not found"** | Run `pip install -r requirements.txt` |
| **Port already in use** | Change port in `app.py` or kill other processes on 5000/3000 |

---

## 📚 Documentation

- **README.md** - This file (overview & quick start)
- **ARCHITECTURE.md** - Technical deep-dive (system design, algorithms)

---

## 🔗 Links

- **Repository:** https://github.com/chetnareddy-2005/PowerSpectrum
- **Report Issues:** GitHub Issues page

---

## 👨‍💻 Author

**Chetna Reddy**  
GitHub: https://github.com/chetnareddy-2005

---

**Last Updated:** June 2026  
**Status:** ✅ Fully Functional with Documentation
