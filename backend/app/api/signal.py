from __future__ import annotations

import logging
import os

from flask import Blueprint, current_app, jsonify, request

from app.services.signal_processing import AnalysisParams, analyze_signal_data

signal_bp = Blueprint("signal", __name__)


def get_int_query_param(name: str, default: int) -> int:
    """Read an integer query parameter with a concrete typed fallback."""
    value = request.args.get(name, default=default, type=int)
    if value is None:
        return default
    return value


def get_str_query_param(name: str, default: str) -> str:
    """Read a string query parameter with a concrete typed fallback."""
    value = request.args.get(name, default=default, type=str)
    if value is None:
        return default
    return value


@signal_bp.route("/upload", methods=["POST"])
def upload_file():
    """Handle file uploads."""
    if "file" not in request.files:
        logging.warning("Upload attempt with no file part.")
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    filename = file.filename
    if not filename:
        logging.warning("Upload attempt with no selected file.")
        return jsonify({"error": "No selected file"}), 400

    upload_folder = str(current_app.config["UPLOAD_FOLDER"])
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    logging.info("File '%s' uploaded successfully.", filename)
    return jsonify({"message": "File uploaded successfully", "filename": filename})


@signal_bp.route("/analyze/<filename>", methods=["GET"])
def analyze_signal_route(filename: str):
    """Analyze the signal and return plots."""
    upload_folder = str(current_app.config["UPLOAD_FOLDER"])
    filepath = os.path.join(upload_folder, filename)
    if not os.path.exists(filepath):
        logging.error(f"Analysis requested for non-existent file: {filename}")
        return jsonify({"error": "File not found"}), 404

    try:
        # Get parameters from request or use defaults
        params: AnalysisParams = {
            "sr": get_int_query_param("sr", 22050),
            "n_fft": get_int_query_param("n_fft", 2048),
            "hop_length": get_int_query_param("hop_length", 512),
            "cmap": get_str_query_param("cmap", "viridis"),
        }

        logging.info("Analyzing '%s' with params: %s", filename, params)

        plots = analyze_signal_data(filepath, params)

        logging.info("Successfully generated plots for '%s'.", filename)
        return jsonify(plots)

    except Exception as error:
        logging.error("Error analyzing file '%s': %s", filename, error, exc_info=True)
        return jsonify({"error": str(error)}), 500
