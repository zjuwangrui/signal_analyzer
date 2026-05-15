from flask import Blueprint, request, jsonify, current_app
from app.services.signal_processing import analyze_signal_data
import os
import logging

signal_bp = Blueprint('signal', __name__)

@signal_bp.route('/upload', methods=['POST'])
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
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        logging.info(f"File '{filename}' uploaded successfully.")
        return jsonify({"message": "File uploaded successfully", "filename": filename})

@signal_bp.route('/analyze/<filename>', methods=['GET'])
def analyze_signal_route(filename):
    """Analyze the signal and return plots."""
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        logging.error(f"Analysis requested for non-existent file: {filename}")
        return jsonify({"error": "File not found"}), 404

    try:
        # Get parameters from request or use defaults
        params = {
            'sr': request.args.get('sr', default=22050, type=int),
            'n_fft': request.args.get('n_fft', default=2048, type=int),
            'hop_length': request.args.get('hop_length', default=512, type=int),
            'win_length': request.args.get('win_length', default=None, type=int),
            'window': request.args.get('window', default='hann', type=str),
            'cmap': request.args.get('cmap', default='viridis', type=str)
        }
        if params['win_length'] is None:
            params['win_length'] = params['n_fft']
        
        logging.info(f"Analyzing '{filename}' with params: {params}")

        plots = analyze_signal_data(filepath, params)
        
        logging.info(f"Successfully generated plots for '{filename}'.")
        return jsonify(plots)

    except Exception as e:
        logging.error(f"Error analyzing file '{filename}': {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
