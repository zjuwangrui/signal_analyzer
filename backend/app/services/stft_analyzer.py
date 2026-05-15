import numpy as np
from scipy.signal import get_window

def stft(y, n_fft=2048, hop_length=512, win_length=None, window='hann'):
    """
    Short-Time Fourier Transform (STFT).
    
    A manual implementation of STFT.
    
    :param y: Input signal (1D numpy array).
    :param n_fft: FFT window size.
    :param hop_length: Hop length between successive frames.
    :param win_length: Each frame of audio is windowed by `window` of length `win_length` and then padded with zeros to match `n_fft`. Defaults to `n_fft`.
    :param window: The window function to use. See `scipy.signal.get_window`.
    :return: A complex-valued matrix D such that D[f, t] is the FFT of frame t at frequency f.
    """
    if win_length is None:
        win_length = n_fft

    # Get the window function
    fft_window = get_window(window, win_length)

    # Pad the window to n_fft size if necessary
    pad_len = n_fft - win_length
    if pad_len < 0:
        raise ValueError("win_length must be smaller than n_fft")
    
    fft_window = np.pad(fft_window, (0, pad_len), mode='constant')

    # Pad the signal to ensure all frames are centered
    y = np.pad(y, int(n_fft // 2), mode='reflect')

    # Calculate the number of frames
    n_frames = 1 + int((len(y) - n_fft) / hop_length)
    
    # Initialize the STFT matrix
    stft_matrix = np.empty((1 + n_fft // 2, n_frames), dtype=np.complex64, order='F')

    # Iterate over frames
    for t in range(n_frames):
        start = t * hop_length
        frame = y[start : start + n_fft]
        
        # Window the frame and compute FFT
        windowed_frame = frame * fft_window
        stft_matrix[:, t] = np.fft.rfft(windowed_frame)

    return stft_matrix
