# 🚀 PowerSpectrum – Radar Signal Processing & Spectral Analysis System

## 📌 Overview

PowerSpectrum is a radar signal processing and spectral analysis application designed to process radar data, calculate spectral characteristics and detectability metrics, and visualize radar beam characteristics through a web interface.

The system combines a **Python Flask backend** for radar-file processing with a **React-based FFT Plotter** for I/Q frequency-spectrum visualization.

**Validation status:** The available evaluation reported 40/40 passing synthetic unit tests and successful processing of three incoherent-average radar files. However, critical issues remain in the source audit. The current results do not establish that every application path or every supported file format is correct.

---

## 🎯 Three Core Modules

| Module | Purpose | Input | Output | Technology |
|---|---|---|---|---|
| **Spectral Data Viewer** | Radar analysis engine | Compatible radar files | Spectral metrics and detectability graphs | Python, NumPy, Matplotlib |
| **FFT Plotter** | I/Q frequency visualization | I/Q signal samples | Frequency-spectrum graph | React, Plotly.js, Flask API |
| **Radar Graph Viewer** | Web-based results dashboard | Reference and test radar files | E-W, N-S, and detectability graphs | Flask, HTML/CSS, Matplotlib |

## 🏗️ How They Work Together

### Spectral Data Viewer and Radar Graph Viewer

```text
Compatible incoherent-average radar file
        ↓
Spectral Data Viewer
        ↓
Read binary header and precomputed power spectra
        ↓
Calculate spectral moments, SNR, and detectability
        ↓
Generate Matplotlib figures
        ↓
Radar Graph Viewer dashboard
```

### FFT Plotter

```text
I/Q signal samples
        ↓
User enters I and Q values
        ↓
React FFT Plotter
        ↓
Flask /process API
        ↓
Complex signal construction and FFT
        ↓
Frequency-spectrum graph
```

**Important:** The source audit identified two separate processing paths. The Flask pipeline reads precomputed `float32` power spectra from compatible incoherent-average files. Standalone scripts process raw `int16` I/Q data from coherent `.r12` files. These paths are not interchangeable.

---

## 🎯 Key Features

### Radar Data Processing
- Binary radar header parsing.
- Reference and test dataset processing.
- Multi-beam radar analysis.
- Spectral analysis for compatible incoherent-average data.

### Signal Analysis
- FFT-based spectral analysis in the applicable processing path.
- Spectral moment calculations.
- Total-power computation.
- SNR estimation.
- Detectability calculations and graph generation.

### Multi-Beam Radar Analysis

The application is designed to analyze five radar beams:

1. East Beam
2. West Beam
3. Zenith Beam
4. North Beam
5. South Beam

Every beam and file format must be validated against the actual input layout before its results are treated as scientifically reliable.

### Generated Visualizations
- E-W reference-versus-test spectra.
- N-S reference-versus-test spectra.
- Detectability profiles and SNR metrics.
- Beam-wise detectability comparisons where supported.

---

## 📊 Evaluation Results and Metrics

The following values are taken from the available evaluation report. They describe the reported test environment and tested files, not a universal performance guarantee.

### Synthetic Unit Tests

| Metric | Result |
|---|---:|
| Synthetic unit tests passed | **40/40** |
| Reported test duration | **0.36 seconds** |
| Real-data files processed successfully | **3** |
| NaN values reported in checked processing runs | **0** |

The tests covered:

- Frequency-axis and sampling-frequency formulas.
- FFT outputs, Parseval checks, and peak locations.
- Spectral moments, SNR, and total power.
- Edge cases involving NaN, infinity, and empty input.
- Doppler-axis and velocity conversion.
- Binary-header parsing.

Run the tests from the evaluation directory:

```bash
python -m pytest test_signal_processing.py -v
```

**Note:** The 40/40 result applies to the reported synthetic unit-test suite. It does not prove that every production code path, web route, binary format, or numerical formula has been validated.

### Real-Data Processing and Latency

| Radar File | Reported Median Latency |
|---|---:|
| `6JL2019SHT1Incoh.d2` | **17.5 ms** |
| `12AU2025SHT1Incoh.d1` | **13.9 ms** |
| `9JL2025SHT1Incoh.d11` | **14.8 ms** |

The evaluation report states that the benchmark included file I/O and used repeated runs.

**Matplotlib rendering:** Approximately **500 ms** was identified as a likely major contributor to full web-request latency. This is an approximate figure from the supplied report and should be remeasured using an end-to-end benchmark before being treated as a guaranteed application latency.

### Evaluated Input Files

| File | Reported Size | NRGB | NFFT | IPP (µs) | Frames | Reported Status |
|---|---:|---:|---:|---:|---:|---|
| `6JL2019SHT1Incoh.d2` | 6.26 MB | 160 | 256 | 180 | 40 | Flask-compatible in the evaluated pipeline |
| `12AU2025SHT1Incoh.d1` | 7.66 MB | 140 | 256 | 160 | 56 | Flask-compatible in the evaluated pipeline |
| `9JL2025SHT1Incoh.d11` | 6.98 MB | 140 | 256 | 160 | 51 | Flask-compatible in the evaluated pipeline |
| `9JL2025SHT1.d11` (coherent) | 27.9 MB | — | — | — | 203 | Not compatible with the current Flask parser; silent corruption risk reported |
| `23JU2025SHT1.r12` (raw I/Q) | 42.9 MB | — | — | — | 313 | Not compatible with the current Flask parser; silent corruption risk reported |

The sizes, frame counts, and latency values above come from the supplied evaluation report. Re-run the benchmark to confirm them for a different machine or code revision.

---

## 🧪 Validation Methodology

The reported evaluation included:

1. Source inspection of `app.py`, `data.py`, `moments.py`, `spectral_data_detectability.py`, and `rawdata.py`.
2. Synthetic unit tests for signal-processing formulas and edge cases.
3. Binary-header and file-inventory checks.
4. Real-data processing checks for three incoherent-average files.
5. Repeated-run latency benchmarks.
6. A read-only source audit that reported no modifications to application code, raw radar files, or reference CSVs during that evaluation.

The evaluation report lists these artifacts under `evaluation/`:

- `audit_report.md`
- `evaluation_summary.md`
- `methodology.md`
- `missing_requirements.md`
- `test_signal_processing.py`
- `benchmark_radar.py`
- `signal_processing_test_results.csv`
- `signal_processing_test_results.json`
- `benchmark_results.csv`
- `benchmark_results.json`
- `mst_radar_evaluation.md`

Confirm that these files exist in the current repository before relying on them.

---

## ⚠️ Known Issues and Required Corrections

The supplied evaluation report identified the following issues. Confirm them against the current source before applying fixes.

| ID | Severity | Location | Reported Issue | Required Follow-Up |
|---|---|---|---|---|
| **B1** | High | `moments.py:64` | `sn*2` was reported where `sn**2` was expected, potentially causing incorrect spectral-width convergence behavior. | Verify the intended formula, correct it if confirmed, and add regression tests. |
| **B3** | High | `spectral_data_detectability.py` | Coherent `.d11` and raw `.r12` inputs were reportedly read as `float32` despite containing raw `int16` I/Q data. | Reject incompatible inputs or implement separately validated parsers. |
| **B4** | Medium | `spectral_data_detectability.py:15,70` | File handles opened without context managers create a file-descriptor leak risk. | Use `with open(...)` and test error paths. |
| **B5** | Medium | `spectral_data_detectability.py:20` | `nici` was reportedly hard-coded to `1`, while the inspected header indicated `4`. | Confirm parameter semantics and validate the correct header field. |
| **B6** | Medium | `app.py:50` | A relative default reference-file path may fail when the application starts from another working directory. | Resolve paths from a stable project/configuration directory and test startup elsewhere. |

**These issues must not be described as fixed unless the code has actually been changed and the relevant regression tests pass.** The reported 40/40 synthetic tests do not establish that these application-level issues are resolved.

### File-Format Safety

Until B3 is fixed and tested, do not process coherent `.d11` or raw `.r12` files through the current Flask parser. Use only input files whose compatibility has been verified.

A file extension alone does not prove that the binary parser is correct.

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

```

This is a representative structure based on the supplied README and evaluation report. Actual files may differ between repository versions.

---

## ⚙️ Installation and Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/chetnareddy-2005/PowerSpectrum.git
cd PowerSpectrum
```

### Step 2: Create Python Environment

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
python -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

The original README lists:

```text
Flask==3.0.0
flask-cors==4.0.0
matplotlib==3.8.0
numpy>=1.24.0
```

Use the current repository's `requirements.txt` as the source of truth if it differs.

### Step 4: Verify Sample Data

Confirm that the chosen reference and test files exist and are compatible with the current parser. Do not use coherent `.d11` or `.r12` files through the Flask parser until B3 is resolved and validated.

---

## ▶️ Running the Application

### Option A: Radar Graph Viewer

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

The dashboard is intended to support reference/test uploads, processing, and graph tabs. Test the full upload flow after the known parser and path issues are addressed.

### Option B: FFT Plotter and Backend

**Terminal 1:**

```bash
python app.py
```

**Terminal 2:**

```bash
cd fft-plotter
npm install
npm start
```

Open:

```text
http://localhost:3000
```

Example input:

```text
I = 1,2,3,4
Q = 3,4,5,6
```

Click **Plot Graph** to view the frequency spectrum. Verify that the frontend reaches the Flask `/process` endpoint and inspect browser/API errors if the graph does not render.

### Option C: Direct Processing

The original README documented this example:

```bash
python -c "from spectral_data_detectability import process_files; process_files('6JL2019SHT1Incoh.d2', '9JL2025SHT1.d11')"
```

**Caution:** The supplied evaluation report identifies `9JL2025SHT1.d11` as a coherent file incompatible with the current Flask parser. Do not use this example unchanged until B3 is fixed. Select a verified compatible incoherent-average file for testing.

---

## 📈 Module Details

### Module 1: Spectral Data Viewer

Relevant files:

- `spectral_data_detectability.py` — Flask processing pipeline.
- `moments.py` — spectral moment calculations.
- `rawdata.py` — raw-data parsing utilities.
- `data.py` — data-loading and standalone processing utilities.

For compatible incoherent-average data, the reported Flask pipeline:

1. Reads the binary header.
2. Extracts parameters such as range-bin count, FFT size, IPP, and integration count.
3. Reads precomputed power spectra.
4. Calculates spectral characteristics and moments.
5. Estimates noise, SNR, and detectability.
6. Generates E-W, N-S, and detectability figures.

The standalone raw-I/Q path is separate and must not be assumed to use the same input format.

### Module 2: FFT Plotter

The described implementation constructs a complex signal from I/Q arrays and calculates the FFT:

```python
signal = I + 1j * Q
fft_values = np.fft.fft(signal)
magnitude = np.abs(fft_values)
frequency = np.fft.fftfreq(len(signal))
```

The frontend plots frequency against magnitude. Validate I/Q array lengths, empty inputs, and API error handling.

### Module 3: Radar Graph Viewer

The dashboard uses Flask routes and Matplotlib-generated figures to display radar comparisons. Visual styling does not establish numerical correctness; validate the processing outputs separately.

---

## 💻 Technology Stack

### Backend
- Python
- Flask
- NumPy
- Matplotlib
- Flask-CORS

### Frontend
- HTML/CSS
- React
- Plotly.js
- JavaScript

### Data Formats
- `.d1`, `.d2`, `.d11` — compatibility depends on the actual binary layout and parser.
- `.r12` — raw I/Q format handled by a separate standalone processing path in the audited implementation.
- `.csv` — reference metrics and analysis outputs.

Never infer file compatibility from its extension alone.

---

## 🎓 Applications

- Radar signal processing.
- Spectral analysis and visualization.
- Signal detectability studies.
- Atmospheric radar research and development.
- Digital signal processing education.
- Reference-versus-test radar measurement comparison.

---

## 🔍 Common Use Cases

### Compare Radar Measurements

1. Select a reference file and a compatible test file.
2. Upload and process them through the dashboard.
3. Inspect E-W, N-S, and detectability graphs.
4. Review the source data and processing assumptions before drawing scientific conclusions.

### Visualize an I/Q Frequency Spectrum

1. Open the FFT Plotter.
2. Enter I and Q sample arrays.
3. Submit the input.
4. Inspect the frequency-spectrum graph and API response.

### Test Signal-Processing Behavior

1. Run the synthetic unit tests.
2. Run the benchmark script against available files.
3. Compare results with the evaluation report.
4. Record the environment and code revision for reproducibility.

---

## 📝 Interview Explanation

### Quick Pitch

> PowerSpectrum is a radar signal analysis platform with a Flask-based processing engine, a React FFT Plotter, and a web dashboard. The analysis engine processes compatible incoherent-average radar spectra, calculates spectral characteristics and detectability metrics, and generates multi-beam visualizations. The FFT Plotter accepts I/Q samples and displays their frequency spectrum.

### Technical Explanation

> The system contains two distinct signal-processing paths. The Flask pipeline reads precomputed float32 power spectra from compatible incoherent-average files and calculates moments, SNR, and detectability for visualization. Separate standalone utilities handle raw int16 I/Q data and FFT processing. The available evaluation recorded 40/40 passing synthetic tests and median processing latencies of 13.9–17.5 ms for three tested incoherent-average files. However, the source audit identified formula, file-format, file-handle, header-parameter, and relative-path issues that require correction and regression testing before the entire application can be described as fully validated.

---

## 🐛 Troubleshooting

| Issue | Suggested Check |
|---|---|
| File not found | Confirm the file exists and resolve its path independently of the current working directory. |
| FFT Plotter blank page | Confirm Flask and React are running; inspect browser console and network errors. |
| CORS errors | Verify Flask-CORS configuration and the frontend API URL. |
| Module not found | Activate the intended virtual environment and install repository dependencies. |
| Port already in use | Identify the process using the port before changing configuration. |
| Strange spectra from `.r12` or coherent `.d11` | Stop using the current Flask parser for these formats; investigate B3. |
| Incorrect spectral-width results | Investigate B1 and add regression tests before relying on the values. |
| Different behavior from another working directory | Investigate B6 and resolve paths from a stable base directory. |
| Unexpected scan/integration counts | Investigate B5 and verify header-field semantics. |

---

## 📚 Documentation

- `README.md` — project overview, setup, metrics, and limitations.
- `ARCHITECTURE.md` — technical architecture.
- `evaluation/audit_report.md` — source audit findings, if present.
- `evaluation/evaluation_summary.md` — consolidated results, if present.
- `evaluation/methodology.md` — evaluation methodology, if present.
- `evaluation/missing_requirements.md` — outstanding requirements, if present.
- `evaluation/mst_radar_evaluation.md` — detailed evaluation report, if present.

---

## 🔗 Links

- **Repository:** https://github.com/chetnareddy-2005/PowerSpectrum
- **Issues:** Use the repository's GitHub Issues page.

---

## 👨‍💻 Author

**Chetna Reddy**  
GitHub: https://github.com/chetnareddy-2005

---

## 📌 Current Status

**Status: Partially evaluated — critical issues remain.**

### Verified in the supplied evaluation report
- 40/40 synthetic unit tests passed in the reported run.
- Three listed incoherent-average files were reported as processed successfully.
- Median processing latency was reported as 13.9 ms, 14.8 ms, and 17.5 ms for the three tested files.
- Matplotlib rendering, at approximately 500 ms, was identified as a likely major contributor to end-to-end latency.

### Outstanding work
- Verify and correct the spectral-width formula (B1).
- Fix or explicitly reject incompatible coherent/raw-IQ inputs in the Flask parser (B3).
- Close files safely (B4).
- Verify the `nici` header parameter (B5).
- Make the default reference path independent of the current working directory (B6).
- Re-run regression tests and end-to-end checks after corrections.
- Confirm evaluation artifacts and metrics correspond to the current repository revision.

**Do not describe the system as fully functional or fully validated until the critical issues have been resolved and the relevant tests have passed.**

**Last updated:** October 2026
