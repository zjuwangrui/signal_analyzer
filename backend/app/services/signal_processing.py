from __future__ import annotations

from typing import TypedDict

import librosa
import librosa.display
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from ..utils.helpers import fig_to_base64
from .stft_analyzer import stft

FloatArray = NDArray[np.float64]


class AnalysisParams(TypedDict):
    sr: int
    n_fft: int
    hop_length: int
    cmap: str


class AnalysisPlots(TypedDict):
    waveform: str
    spectrogram: str
    spectrum: str


def analyze_signal_data(filepath: str, params: AnalysisParams) -> AnalysisPlots:
    """
    Loads an audio file and generates waveform, spectrogram, and spectrum plots.

    :param filepath: Path to the audio file.
    :param params: A dictionary of analysis parameters.
    :return: A dictionary containing base64 encoded plot images.
    """
    y_raw, sr_loaded = librosa.load(filepath, sr=params["sr"])
    y: FloatArray = np.asarray(y_raw, dtype=np.float64)

    # 1. Time-domain waveform
    fig_time, ax_time = plt.subplots(figsize=(10, 4))
    librosa.display.waveshow(y, sr=sr_loaded, ax=ax_time)
    ax_time.set_title('Time-Domain Waveform')
    ax_time.set_xlabel('Time (s)')
    ax_time.set_ylabel('Amplitude')
    img_time = fig_to_base64(fig_time)

    # 2. Spectrogram using the custom STFT
    frequencies, times, spectrum = stft(
        y,
        fs=float(sr_loaded),
        window_size=params["n_fft"],
        frame_shift=params["hop_length"],
    )
    positive_bin_count = params["n_fft"] // 2 + 1
    positive_frequencies = frequencies[:positive_bin_count]
    magnitude = np.abs(spectrum[:positive_bin_count, :])
    S_db = librosa.amplitude_to_db(magnitude, ref=np.max)
    fig_spec, ax_spec = plt.subplots(figsize=(10, 4))
    img = ax_spec.pcolormesh(
        times,
        positive_frequencies,
        S_db,
        shading="auto",
        cmap=params["cmap"],
    )
    ax_spec.set_title("Spectrogram")
    ax_spec.set_xlabel("Time (s)")
    ax_spec.set_ylabel("Frequency (Hz)")
    ax_spec.set_ylim(0, sr_loaded / 2)
    fig_spec.colorbar(img, ax=ax_spec, format="%+2.0f dB")
    img_spectrogram = fig_to_base64(fig_spec)

    # 3. Spectrum Plot
    fft_vals = np.fft.rfft(y)
    fft_freq = np.fft.rfftfreq(len(y), d=1./sr_loaded)
    fig_fft, ax_fft = plt.subplots(figsize=(10, 4))
    ax_fft.plot(fft_freq, np.abs(fft_vals))
    ax_fft.set_title('Spectrum')
    ax_fft.set_xlabel('Frequency (Hz)')
    ax_fft.set_ylabel('Magnitude')
    ax_fft.set_xlim(0, sr_loaded / 2)
    img_spectrum = fig_to_base64(fig_fft)

    return {
        "waveform": img_time,
        "spectrogram": img_spectrogram,
        "spectrum": img_spectrum,
    }
