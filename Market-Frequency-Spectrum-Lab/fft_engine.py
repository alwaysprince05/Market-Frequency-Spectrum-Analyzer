# fft_engine.py
import numpy as np

def compute_fft(data, time, window_size=64, step=16):
    n = len(data)
    spectrum_matrix = []
    freq = np.fft.rfftfreq(window_size, d=(time[1]-time[0]))
    for start in range(0, n-window_size, step):
        window = data[start:start+window_size]
        fft_vals = np.fft.rfft(window)
        amplitude = np.abs(fft_vals)
        spectrum_matrix.append(amplitude)
    spectrum_matrix = np.array(spectrum_matrix)
    # For 2D spectrum plot
    fft_full = np.fft.rfft(data)
    amplitude_full = np.abs(fft_full).flatten()
    freq_full = np.fft.rfftfreq(len(data), d=(time[1]-time[0]))
    # Ensure freq_full and amplitude_full have the same shape
    min_len = min(len(freq_full), len(amplitude_full))
    freq_full = freq_full[:min_len]
    amplitude_full = amplitude_full[:min_len]
    return freq_full, amplitude_full, spectrum_matrix
