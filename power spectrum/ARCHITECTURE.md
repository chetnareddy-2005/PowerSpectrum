# PowerSpectrum Architecture

## System Design

```
┌─────────────────────────────────────────────────────────────────┐
│                      PowerSpectrum System                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐           ┌──────────────────┐          │
│  │  Web UI (HTML)   │           │  FFT Plotter     │          │
│  │  Dashboard       │           │  (React)         │          │
│  └────────┬─────────┘           └────────┬─────────┘          │
│           │                              │                     │
│           └──────────────────┬───────────┘                     │
│                              │                                 │
│                    ┌─────────▼─────────┐                      │
│                    │  Flask API Server │                      │
│                    │  (app.py)         │                      │
│                    └────┬──────┬───┬───┘                      │
│                         │      │   │                           │
│                 ┌───────┘      │   └────────┐                 │
│                 │              │            │                  │
│         ┌───────▼────────┐  ┌──▼────────┐  │                 │
│         │  Process Files │  │ /process  │  │                 │
│         │  Endpoint      │  │ FFT API   │  │                 │
│         └────────┬───────┘  └──┬───────┘   │                 │
│                  │             │           │                  │
│         ┌────────▼──────────┐  │     ┌─────▼─────┐           │
│         │ Spectral Analysis │  │     │   NumPy   │           │
│         │ Engine            │  │     │   FFT     │           │
│         └────────┬──────────┘  │     └───────────┘           │
│                  │             │                               │
│         ┌────────▼────────┐    │                               │
│         │  Results        │    │                               │
│         │  - E-W Graphs   │    │                               │
│         │  - N-S Graphs   │◄───┘                               │
│         │  - Detectability│                                    │
│         │  - SNR Metrics  │                                    │
│         └─────────────────┘                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Module Architecture

### 1. Spectral Data Viewer (Backend Processing)

**File:** `spectral_data_detectability.py`

```python
def process_files(ref_file: str, test_file: str) -> dict:
    """
    Main entry point for radar file processing.

    Flow:
    1. Parse Reference File
       - Read binary header
       - Extract radar parameters (baud, nrgb, nfft, etc.)
       - Calculate sampling frequency: fs = 1e6 / (ipp * nci)
       - Parse all frames

    2. Parse Test File
       - Same structure as reference

    3. For each beam (1-5):
       - For each range bin:
         - Read raw I/Q data
         - Apply FFT
         - Calculate spectral moments
         - Compute detectability

    4. Aggregate Results
       - Generate matplotlib figures
       - Create comparison plots

    Return: {0: fig_ew, 1: fig_ns, 2: fig_detectability}
    """
```

**Key Data Structures:**

```python
# Spectral data: (beams=5, range_bins, fft_size)
spectra = np.zeros((5, nrgb, nfft), dtype=np.float64)

# Detectability: (1, beams=5, range_bins)
detectability = np.zeros((1, 5, nrgb))

# Reference metrics
ew_ref, ns_ref = np.zeros((1, nrgb)), np.zeros((1, nrgb))
snr_list = []
tot_power_list = []
```

**File Format Parsing:**

```
Binary Radar File:
├─ Header (128 bytes = 64 × int16)
│  ├─ A[0]:  Reserved
│  ├─ A[1]:  BAUD (Baud rate)
│  ├─ A[2]:  NRGB (Number of range bins)
│  ├─ A[3]:  NFFT (FFT size)
│  ├─ A[4]:  NCI (Number of coherent integrations)
│  ├─ A[6]:  IPP (Inter-pulse period in µs)
│  ├─ A[20]: NBEAM (Number of beams)
│  └─ ...
│
├─ Frame 1 Data (128 + NRGB × NFFT × 4 bytes)
│  └─ NRGB × NFFT × int32 values (I/Q interleaved or separated)
│
├─ Frame 2 Data
│  └─ ...
│
└─ Frame N Data
```

**Sampling Parameters:**

```python
# Derived from header
Ts = ipp * nci  # Total sampling period (µs)
fs = 1e6 / Ts   # Sampling frequency (Hz)
freq = np.linspace(-fs/2, fs/2, nfft)  # Frequency axis

# Frame properties
frame_length = (ipp / 1e6) * nci * nfft  # Duration (seconds)
frame_size = 128 + nrgb * nfft * 4      # Bytes
```

---

### 2. Moments Calculation

**File:** `moments.py`

```python
class Moments:
    """Compute spectral moments from power spectral density."""

    def compute(self):
        """
        Computes:
        1. Mean frequency (Doppler)
        2. Bandwidth
        3. SNR
        4. Higher-order moments

        Uses:
        - M0 = ∫ S(f) df (total power)
        - M1 = ∫ f·S(f) df (mean frequency)
        - M2 = ∫ f²·S(f) df (variance)
        """
        pass
```

---

### 3. FFT Processing (Frontend Integration)

**Files:**

- `app.py:/process` endpoint
- `fft-plotter/src/App.js`

**Data Flow:**

```
React App
    ↓
User enters I, Q values
    ↓
POST /process
    {
      "I": [1, 2, 3, 4],
      "Q": [3, 4, 5, 6]
    }
    ↓
Flask API Handler
    ├─ signal = I + 1j·Q
    ├─ fft = np.fft.fft(signal)
    ├─ mag = |fft|
    ├─ freq = np.fft.fftfreq(len(signal))
    └─ return {x: freq, y: mag}
    ↓
React
    ├─ Plot with Plotly
    ├─ X-axis: Frequency
    └─ Y-axis: Magnitude
```

---

### 4. Flask Routes

**app.py:**

```python
# Home page - Radar Graph Viewer
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", showgraphs=(len(graphs) > 0))

# File upload and processing
@app.route("/upload", methods=["POST"])
def upload():
    # 1. Receive files from form
    # 2. Save to uploads/
    # 3. Call process_files()
    # 4. Return dashboard with graphs

# Dynamic graph serving (as PNG)
@app.route("/graph/<int:graph_id>", methods=["GET"])
def graph(graph_id):
    # Return cached matplotlib figure as PNG
    fig = graphs[graph_id]
    canvas = FigureCanvas(fig)
    return Response(canvas.to_png(), mimetype="image/png")

# FFT Processing API
@app.route("/process", methods=["POST"])
def process_fft():
    # 1. Get I, Q arrays from JSON
    # 2. Compute FFT
    # 3. Return frequency, magnitude
    return jsonify({"x": freq.tolist(), "y": mag.tolist()})

# File download
@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    return send_from_directory("uploads", filename)
```

---

## Data Processing Pipeline

### Step 1: File Parsing

```python
# Open binary file
with open(radar_file, 'rb') as f:
    # Read header
    header = np.fromfile(f, dtype=np.int16, count=64)
    nrgb = header[2]    # Range bins
    nfft = header[3]    # FFT size
    nbeam = header[20]  # Beams

    # Calculate frame size
    frame_size = nrgb * nfft * 4  # bytes (int32 per sample)

    # Count frames
    f.seek(0, 2)  # End of file
    file_size = f.tell()
    frame_count = (file_size - 128) // (128 + frame_size)
```

### Step 2: Spectral Calculation

```python
for beam in range(nbeam):
    for frame in range(frame_count):
        # Read frame data
        frame_data = np.fromfile(f, dtype=np.int32, count=nrgb*nfft)
        frame_data = frame_data.reshape(nrgb, nfft)

        # Apply FFT
        fft_data = np.fft.fft(frame_data, axis=1)

        # Power spectrum
        psd = np.abs(fft_data) ** 2

        # FFT shift (center frequency)
        psd = np.fft.fftshift(psd, axes=1)

        # Store
        spectra[beam, :, :] = psd
```

### Step 3: Moment Computation

```python
# For each range bin
for rgb in range(nrgb):
    spectrum = spectra[:, rgb, :]  # All beams, this range bin
    freq = np.fft.fftshift(np.fft.fftfreq(nfft, 1/fs))

    # Moments
    m0 = np.sum(spectrum)           # Total power
    m1 = np.sum(freq * spectrum)    # Mean frequency
    m2 = np.sum(freq**2 * spectrum) # Second moment

    # Statistics
    mean_freq = m1 / m0 if m0 > 0 else 0
    bandwidth = np.sqrt((m2 / m0) - (mean_freq ** 2))
    snr = 10 * np.log10(m0)  # Simple SNR estimation
```

### Step 4: Detectability

```python
def compute_detectability(spectrum, threshold=0.5):
    """
    Detect if signal exceeds noise floor.
    """
    # Noise floor estimation
    noise_floor = np.mean(spectrum)

    # Find peaks
    peaks = spectrum > (noise_floor * (1 + threshold))

    # Detectability = % of frequency bins with signal
    detectability = np.sum(peaks) / len(spectrum)

    return detectability
```

---

## Frontend Architecture

### HTML/CSS Structure

**templates/index.html:**

```html
<html>
  <body>
    <!-- Star background -->
    <div class="stars" id="stars-container"></div>

    <!-- Main content -->
    <div class="content-wrapper">
      <!-- Upload form -->
      <form
        id="upload-form"
        enctype="multipart/form-data"
        method="POST"
        action="/upload"
      >
        <div class="container">
          <div class="panel">
            <!-- Reference file input -->
          </div>
          <div class="panel">
            <!-- Test file input -->
          </div>
        </div>
        <button type="submit">Upload & Process</button>
      </form>

      <!-- Results tabs -->
      <div class="tabs" id="graphs">
        <div class="tab-buttons">
          <button class="tab-btn active" data-target="g0">Graph 1</button>
          <button class="tab-btn" data-target="g1">Graph 2</button>
          <button class="tab-btn" data-target="g2">Graph 3</button>
        </div>

        <div class="tab-content active" id="g0">
          <img src="/graph/0?t=" alt="Graph 1" />
        </div>
        <!-- ... -->
      </div>
    </div>

    <script>
      // Star animation (150 stars, 2-5s flicker)
      // Cache busting (add timestamp to img src)
      // Tab switching functionality
    </script>
  </body>
</html>
```

### React FFT Plotter

**fft-plotter/src/App.js:**

```jsx
function App() {
  const [I, setI] = useState("");
  const [Q, setQ] = useState("");
  const [data, setData] = useState(null);

  const handleSubmit = async () => {
    const response = await fetch("http://127.0.0.1:5000/process", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        I: I.split(",").map(Number),
        Q: Q.split(",").map(Number)
      })
    });

    const result = await response.json();
    setData(result);  // {x: freq, y: magnitude}
  };

  return (
    <div>
      <input value={I} onChange={(e) => setI(e.target.value)}
             placeholder="e.g. 1,2,3,4" />
      <input value={Q} onChange={(e) => setQ(e.target.value)}
             placeholder="e.g. 3,4,5,6" />
      <button onClick={handleSubmit}>Plot Graph</button>

      {data && <Plot data={[{x: data.x, y: data.y, ...}]} />}
    </div>
  );
}
```

---

## Deployment Architecture

```
Development:
┌──────────────────┐
│ Local Filesystem │
└────────┬─────────┘
         │
    ┌────▼─────────────────────────────┐
    │ Flask Dev Server (debug=True)    │
    │ http://127.0.0.1:5000            │
    └────┬──────────────────────────────┘
         │
    ┌────▼─────────────────────────────┐
    │ React Dev Server (npm start)     │
    │ http://localhost:3000            │
    └─────────────────────────────────┘
```

---

## Performance Considerations

### Memory

- **Spectrum storage:** 5 beams × 1024 range bins × 1024 FFT size × 8 bytes = ~40 MB per frame
- **Caching:** Keep last 3 graphs in memory (`graphs` dict)

### Processing Time

- **FFT:** O(N log N) where N = nfft (typically 1024)
- **File I/O:** Bottleneck for large files (multiple GB)
- **Matplotlib rendering:** ~500ms per figure

### Optimization

- Use `numpy.fft` (C-based implementation)
- Cache FFT plans for repeated sizes
- Stream file processing instead of loading entire file

---

## Error Handling

```
┌─────────────────────────────┐
│  User Request               │
└────────────┬────────────────┘
             │
      ┌──────▼──────────┐
      │ Validate Input  │
      └──────┬──────────┘
             │
      ┌──────▼──────────┐
      │ Try Processing  │
      └──────┬──────────┘
             │
        ┌────┴────┐
        │          │
    Success     Exception
        │          │
        │    ┌─────▼──────────┐
        │    │ Log Error      │
        │    ├─────────────────┤
        │    │ Return 500 JSON │
        │    └────────────────┘
        │
    ┌───▼──────────────┐
    │ Return Results   │
    └──────────────────┘
```

---

## Security Considerations

1. **File Upload:**
   - Validate file extensions (.d1, .d2, .r12)
   - Store in isolated `uploads/` directory
   - Clean up old files periodically

2. **API:**
   - CORS enabled (check origin if in production)
   - Input validation on I/Q arrays
   - Error messages don't leak system info

3. **Dependencies:**
   - Pin versions in requirements.txt
   - Regular security updates

---

## Testing Strategy

```python
# Unit tests for moments calculation
def test_moments_computation():
    pass

# Integration tests for file parsing
def test_radar_file_parsing():
    pass

# API tests
def test_fft_endpoint():
    pass

# Frontend tests (Jest)
# End-to-end tests (Selenium)
```

---

**Last Updated:** June 2026
