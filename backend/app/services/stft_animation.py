from __future__ import annotations

import os
from typing import TypedDict

import librosa
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from .stft_analyzer import stft as manual_stft


class AnimationParams(TypedDict):
    sr: int
    n_fft: int
    hop_length: int
    cmap: str
    frame_nums: int


class AnimationResult(TypedDict):
    filename: str
    url: str


def create_spectrogram_animation(
    input_path: str,
    output_dir: str,
    filename: str,
    sr: int = 44100,
    n_fft: int = 2048,
    hop_length: int = 512,
    cmap: str = "magma",
    frame_nums: int = 10,
) -> str:
    """Render a silent STFT animation."""
    os.makedirs(output_dir, exist_ok=True)

    y, sr = librosa.load(input_path, sr=sr)
    frequencies, _, stft_result = manual_stft(
        y,
        float(sr),
        window_size=n_fft,
        frame_shift=hop_length,
    )
    positive_bin_count = n_fft // 2 + 1
    positive_frequencies = frequencies[:positive_bin_count]
    stft_magnitude = np.abs(stft_result[:positive_bin_count, :])
    D = librosa.amplitude_to_db(stft_magnitude, ref=np.max)
    max_frequency = float(positive_frequencies[-1])
    fig, ax = plt.subplots(figsize=(12, 7))

    img = ax.imshow(
        D[:, :1],
        aspect="auto",
        origin="lower",
        cmap=cmap,
        extent=[0, hop_length / sr, 0, max_frequency],
    )
    ax.set_ylim(1, max_frequency)
    ax.set_yscale("log")
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set_axis_off()

    def update(frame: int) -> tuple[plt.Artist, ...]:
        start_frame = max(0, frame - frame_nums // 2)
        end_frame = start_frame + frame_nums

        if end_frame > D.shape[1]:
            end_frame = D.shape[1]
            start_frame = max(0, end_frame - frame_nums)

        start_time = start_frame * hop_length / sr
        end_time = end_frame * hop_length / sr
        img.set_data(D[:, start_frame:end_frame])
        img.set_extent([start_time, end_time, 0, max_frequency])
        ax.set_xlim(start_time, end_time)
        return (img,)

    num_frames = D.shape[1]
    fps = sr / hop_length
    ani = animation.FuncAnimation(
        fig,
        update,
        frames=num_frames,
        blit=True,
        interval=hop_length / sr * 1000,
    )

    output_path = os.path.join(output_dir, filename)
    ani.save(output_path, writer="ffmpeg", fps=int(fps))
    plt.close(fig)
    return output_path
