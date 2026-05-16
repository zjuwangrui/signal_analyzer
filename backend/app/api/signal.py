from __future__ import annotations

import logging
import os
from pathlib import Path
from uuid import uuid4

from flask import Blueprint, current_app, jsonify, request, send_from_directory

from app.services.signal_processing import AnalysisParams, analyze_signal_data
from app.services.stft_animation import AnimationParams, create_spectrogram_animation

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


def build_animation_params() -> AnimationParams:
    """Read animation parameters from the query string."""
    return {
        "sr": get_int_query_param("sr", 44100),
        "n_fft": get_int_query_param("n_fft", 2048),
        "hop_length": get_int_query_param("hop_length", 512),
        "cmap": get_str_query_param("cmap", "magma"),
        "frame_nums": get_int_query_param("frame_nums", 10),
    }


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


@signal_bp.route("/animate/<filename>", methods=["POST"])
def animate_signal_route(filename: str):
    """Generate an STFT animation for an uploaded audio file."""
    upload_folder = str(current_app.config["UPLOAD_FOLDER"])
    filepath = os.path.join(upload_folder, filename)
    if not os.path.exists(filepath):
        logging.error("Animation requested for non-existent file: %s", filename)
        return jsonify({"error": "File not found"}), 404

    try:
        params = build_animation_params()
        if params["n_fft"] <= 0:
            return jsonify({"error": "n_fft must be positive"}), 400
        if params["hop_length"] <= 0:
            return jsonify({"error": "hop_length must be positive"}), 400
        if params["frame_nums"] <= 0:
            return jsonify({"error": "frame_nums must be positive"}), 400

        animation_folder = str(current_app.config["ANIMATION_FOLDER"])
        source_stem = Path(filename).stem
        animation_filename = f"{source_stem}_{uuid4().hex}_stft.mp4"
        create_spectrogram_animation(
            input_path=filepath,
            output_dir=animation_folder,
            filename=animation_filename,
            sr=params["sr"],
            n_fft=params["n_fft"],
            hop_length=params["hop_length"],
            cmap=params["cmap"],
            frame_nums=params["frame_nums"],
        )

        video_url = f"/animations/{animation_filename}"
        download_url = f"/animations/{animation_filename}/download"
        logging.info("Successfully generated animation for '%s': %s", filename, animation_filename)
        return jsonify({"filename": animation_filename, "url": video_url, "download_url": download_url})

    except Exception as error:
        logging.error("Error generating animation for '%s': %s", filename, error, exc_info=True)
        return jsonify({"error": str(error)}), 500


@signal_bp.route("/animations/<filename>", methods=["GET"])
def get_animation_file(filename: str):
    """Serve generated STFT animation files."""
    animation_folder = str(current_app.config["ANIMATION_FOLDER"])
    return send_from_directory(animation_folder, filename, mimetype="video/mp4")


@signal_bp.route("/animations/<filename>/download", methods=["GET"])
def download_animation_file(filename: str):
    """Download a generated STFT animation file."""
    animation_folder = str(current_app.config["ANIMATION_FOLDER"])
    return send_from_directory(
        animation_folder,
        filename,
        mimetype="video/mp4",
        as_attachment=True,
        download_name=filename,
    )
