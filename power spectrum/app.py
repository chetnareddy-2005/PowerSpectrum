import os
import io
from flask import Flask, request, Response, send_from_directory, render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from spectral_data_detectability import process_files

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DEFAULT_REF_FILE = "6JL2019SHT1Incoh.d2"

graphs = {}

# Home page

@app.route("/")
def index():
    return render_template(
        "index.html",
        showgraphs=(len(graphs) > 0)
    )

# Upload and process files

@app.route("/upload", methods=["POST"])
def upload():
    print("---- DEBUG: Upload request received ----")
    print("Form keys:", request.files.keys())

    ref_file = request.files.get("ref_file")
    test_file = request.files.get("test_file")

    if not test_file:
        return "Please upload a test file", 400

    # Save test file
    test_path = os.path.join(UPLOAD_FOLDER, test_file.filename)
    test_file.save(test_path)

    # Save reference file if uploaded
    if ref_file and ref_file.filename.strip():
        ref_path = os.path.join(UPLOAD_FOLDER, ref_file.filename)
        ref_file.save(ref_path)
    else:
        ref_path = DEFAULT_REF_FILE

    global graphs
    graphs = process_files(ref_path, test_path)

    print("Graphs generated successfully")

    return render_template(
        "index.html",
        showgraphs=True
    )


# Dynamic graph route

@app.route("/graph/<int:graph_id>")
def graph(graph_id):
    if graph_id not in graphs:
        return "Graph not found", 404

    fig = graphs[graph_id]

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    return Response(
        output.getvalue(),
        mimetype="image/png"
    )


# Download saved files

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )

if __name__ == "__main__":
    app.run(debug=True)
