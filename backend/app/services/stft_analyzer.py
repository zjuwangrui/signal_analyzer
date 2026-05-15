from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray

FloatArray = NDArray[np.float64]
ComplexArray = NDArray[np.complex128]


def stft(
    signal: ArrayLike,
    fs: float,
    window_size: int,
    frame_shift: int | None = None,
) -> tuple[FloatArray, FloatArray, ComplexArray]:
    """
    Compute STFT with manual framing, rectangular windowing, and per-frame FFT.

    This mirrors the project-level ``stft_analyzer.py`` implementation:
    no centered padding, full FFT output, and a rectangular analysis window.
    ``frame_shift`` defaults to half-window overlap.
    """
    samples: FloatArray = np.asarray(signal, dtype=np.float64).reshape(-1)
    if samples.size == 0:
        raise ValueError("Input signal must not be empty.")
    if fs <= 0:
        raise ValueError("Sampling rate must be positive.")
    if window_size <= 0:
        raise ValueError("Window size must be positive.")
    if window_size > samples.size:
        raise ValueError("Window size must not exceed signal length.")

    if frame_shift is None:
        frame_shift = max(window_size // 2, 1)
    if frame_shift <= 0:
        raise ValueError("Frame shift must be positive.")

    nfft = window_size
    num_frames = (samples.size - window_size) // frame_shift + 1
    window = np.ones(window_size, dtype=np.float64)

    spectrum = np.zeros((nfft, num_frames), dtype=np.complex128)
    frequencies = np.arange(nfft, dtype=np.float64) * fs / nfft

    for frame_index in range(num_frames):
        start_index = frame_index * frame_shift
        end_index = start_index + window_size
        frame = samples[start_index:end_index] * window
        spectrum[:, frame_index] = np.fft.fft(frame, n=nfft)

    times = (np.arange(num_frames, dtype=np.float64) * frame_shift + window_size / 2) / fs
    return frequencies, times, spectrum
