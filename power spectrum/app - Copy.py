import os
import io
from flask import Flask, request, redirect, url_for, Response, send_from_directory
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from spectral_data_detectability import process_files


# Flask setup
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DEFAULT_REF_FILE = "6JL2019SHT1Incoh.d2"  # fallback reference file
graphs = {}

# Routes
@app.route("/")
def index():
    return open("index.html").read()

@app.route("/upload", methods=["POST"])
def upload():
    print("---- DEBUG: Upload request received ----")
    print("Form keys:", request.files.keys())
    print("Ref file:", request.files.get("ref_file"))
    print("Test file:", request.files.get("test_file"))

    ref_file = request.files.get("ref_file")
    test_file = request.files.get("test_file")

    if not test_file:
        print("No test_file uploaded")
        return "Please upload a test file", 400

    # Save uploaded test file
    test_path = os.path.join(UPLOAD_FOLDER, test_file.filename)
    test_file.save(test_path)
    print(f"Test file saved at {test_path}")

    # Save reference file (if provided) or use default
    if ref_file and ref_file.filename.strip() != "":
        ref_path = os.path.join(UPLOAD_FOLDER, ref_file.filename)
        ref_file.save(ref_path)
        print(f"Reference file saved at {ref_path}")
    else:
        ref_path = DEFAULT_REF_FILE
        print(f"No reference file uploaded, using default: {ref_path}")

    # Process files
    global graphs
    graphs = process_files(ref_path, test_path)
    print("Graphs generated")

    return redirect(url_for("index"))

@app.route("/graph/<int:graph_id>")
def graph(graph_id):
    if graph_id not in graphs:
        return "Graph not found", 404
    fig = graphs[graph_id]
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")

# New route to serve saved PNG files
@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Run
if __name__ == "__main__":
    app.run(debug=True)