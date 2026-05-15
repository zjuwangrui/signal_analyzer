import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from ..utils.helpers import fig_to_base64
from .stft_analyzer import stft

def analyze_signal_data(filepath, params):
    """
    Loads an audio file and generates waveform, spectrogram, and spectrum plots.
    
    :param filepath: Path to the audio file.
    :param params: A dictionary of analysis parameters.
    :return: A dictionary containing base64 encoded plot images.
    """
    y, sr_loaded = librosa.load(filepath, sr=params['sr'])

    # 1. Time-domain waveform
    fig_time, ax_time = plt.subplots(figsize=(10, 4))
    librosa.display.waveshow(y, sr=sr_loaded, ax=ax_time)
    ax_time.set_title('Time-Domain Waveform')
    ax_time.set_xlabel('Time (s)')
    ax_time.set_ylabel('Amplitude')
    img_time = fig_to_base64(fig_time)

    # 2. Spectrogram using the custom STFT
    D = stft(y, n_fft=params['n_fft'], hop_length=params['hop_length'], win_length=params['win_length'], window=params['window'])
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    fig_spec, ax_spec = plt.subplots(figsize=(10, 4))
    img = librosa.display.specshow(S_db, sr=sr_loaded, hop_length=params['hop_length'], 
                                   x_axis='time', y_axis='log', ax=ax_spec, cmap=params['cmap'])
    fig_spec.colorbar(img, ax=ax_spec, format='%+2.0f dB')
    ax_spec.set_title('Spectrogram')
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
        "spectrum": img_spectrum
    }
