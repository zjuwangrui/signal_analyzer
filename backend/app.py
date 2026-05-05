import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

# --- Configuration ---
UPLOAD_FOLDER = 'uploads'
LOG_FOLDER = 'logs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

# --- App Initialization ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

# --- Logging Setup ---
logging.basicConfig(
    filename=os.path.join(LOG_FOLDER, 'app.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- Helper Functions ---
def fig_to_base64(fig):
    """Convert a matplotlib figure to a base64 encoded string."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

# --- API Endpoints ---
@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads."""
    if 'file' not in request.files:
        logging.warning("Upload attempt with no file part.")
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        logging.warning("Upload attempt with no selected file.")
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        logging.info(f"File '{filename}' uploaded successfully.")
        return jsonify({"message": "File uploaded successfully", "filename": filename})

@app.route('/analyze/<filename>', methods=['GET'])
def analyze_signal(filename):
    """Analyze the signal and return plots."""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        logging.error(f"Analysis requested for non-existent file: {filename}")
        return jsonify({"error": "File not found"}), 404

    try:
        # --- Get parameters from request or use defaults ---
        sr = request.args.get('sr', default=22050, type=int)
        n_fft = request.args.get('n_fft', default=2048, type=int)
        hop_length = request.args.get('hop_length', default=512, type=int)
        cmap = request.args.get('cmap', default='viridis', type=str)
        # window_size is often n_fft, but can be specified separately.
        # Here we assume it's controlled by n_fft for simplicity.
        
        logging.info(
            f"Analyzing '{filename}' with params: sr={sr}, n_fft={n_fft}, "
            f"hop_length={hop_length}, cmap='{cmap}'"
        )

        # --- Load audio file ---
        y, sr_loaded = librosa.load(filepath, sr=sr)

        # --- 1. Time-domain waveform ---
        fig_time, ax_time = plt.subplots(figsize=(10, 4))
        librosa.display.waveshow(y, sr=sr_loaded, ax=ax_time)
        ax_time.set_title('Time-Domain Waveform')
        ax_time.set_xlabel('Time (s)')
        ax_time.set_ylabel('Amplitude')
        img_time = fig_to_base64(fig_time)

        # --- 2. Spectrogram ---
        D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
        S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
        fig_spec, ax_spec = plt.subplots(figsize=(10, 4))
        img = librosa.display.specshow(S_db, sr=sr_loaded, hop_length=hop_length, 
                                       x_axis='time', y_axis='log', ax=ax_spec, cmap=cmap)
        fig_spec.colorbar(img, ax=ax_spec, format='%+2.0f dB')
        ax_spec.set_title('Spectrogram')
        img_spectrogram = fig_to_base64(fig_spec)

        # --- 3. Spectrum Plot ---
        fft_vals = np.fft.rfft(y)
        fft_freq = np.fft.rfftfreq(len(y), d=1./sr_loaded)
        fig_fft, ax_fft = plt.subplots(figsize=(10, 4))
        ax_fft.plot(fft_freq, np.abs(fft_vals))
        ax_fft.set_title('Spectrum')
        ax_fft.set_xlabel('Frequency (Hz)')
        ax_fft.set_ylabel('Magnitude')
        ax_fft.set_xlim(0, sr_loaded / 2)
        img_spectrum = fig_to_base64(fig_fft)

        logging.info(f"Successfully generated plots for '{filename}'.")
        return jsonify({
            "waveform": img_time,
            "spectrogram": img_spectrogram,
            "spectrum": img_spectrum
        })

    except Exception as e:
        logging.error(f"Error analyzing file '{filename}': {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/images/<filename>')
def get_image(filename):
    # This is a placeholder if you decide to save images on disk and serve them.
    # The current implementation sends images as base64 strings.
    return send_from_directory('path_to_saved_images', filename)

# --- Main Execution ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
