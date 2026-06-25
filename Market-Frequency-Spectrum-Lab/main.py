# Market-Frequency-Spectrum-Lab
# Entry point for running the analysis and visualization

from data_loader import load_data
from fft_engine import compute_fft
from visualization import plot_3d_spectrum, plot_2d_signal, plot_2d_spectrum, animate_3d_spectrum


def main():
    # Use synthetic data for dense signal
    data, time = load_data(source='synthetic')
    # Compute FFT with larger window and smaller step for dense surface
    freq, amplitude, spectrum_matrix = compute_fft(data, time, window_size=128, step=8)
    # 2D Plots
    plot_2d_signal(time, data)
    plot_2d_spectrum(freq, amplitude)
    # 3D Spectrum
    plot_3d_spectrum(spectrum_matrix, time, freq)
    # Animation
    animate_3d_spectrum(spectrum_matrix, time, freq)

if __name__ == "__main__":
    main()
