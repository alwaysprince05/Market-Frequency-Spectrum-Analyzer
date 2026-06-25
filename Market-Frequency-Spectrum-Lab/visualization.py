# visualization.py
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
from matplotlib.animation import FuncAnimation


def plot_2d_signal(time, data):
    plt.figure(figsize=(8, 4))
    plt.plot(time, data, color='blue')
    plt.title('Original Price Signal')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_2d_spectrum(freq, amplitude):
    plt.figure(figsize=(8, 4))
    plt.plot(freq, amplitude, color='red')
    plt.title('Frequency Spectrum')
    plt.xlabel('Frequency')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_3d_spectrum(spectrum_matrix, time, freq):
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    # Quant-style, dark, neon, scientific 3D plot
    if spectrum_matrix.ndim == 1:
        spectrum_matrix = np.expand_dims(spectrum_matrix, axis=0)
    if spectrum_matrix.size == 0:
        print("Spectrum matrix is empty. Cannot plot 3D surface.")
        return
    n_windows, n_freqs = spectrum_matrix.shape
    if n_windows == 0 or n_freqs == 0:
        print("Spectrum matrix has zero dimension. Cannot plot 3D surface.")
        return
    X, Y = np.meshgrid(np.arange(n_windows), np.arange(n_freqs))
    Z = spectrum_matrix.T
    if Z.shape != X.shape:
        min_shape = (min(Z.shape[0], X.shape[0]), min(Z.shape[1], X.shape[1]))
        Z = Z[:min_shape[0], :min_shape[1]]
        X = X[:min_shape[0], :min_shape[1]]
        Y = Y[:min_shape[0], :min_shape[1]]
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    fig.patch.set_facecolor('#181818')
    ax.set_facecolor('#181818')
    ax.grid(color='#444444', linestyle='--', linewidth=0.5)
    # Neon wireframe
    ax.plot_wireframe(X, Y, Z, color='#00FFCC', linewidth=0.7, alpha=0.7)
    # Neon surface (transparent)
    surf = ax.plot_surface(X, Y, Z, cmap=cm.cool, edgecolor='none', linewidth=0, antialiased=True, alpha=0.3)
    # Contour lines
    ax.contour(X, Y, Z, zdir='z', offset=np.min(Z)-0.2, cmap='spring', linewidths=1.2)
    ax.set_title('Quant 3D Frequency Spectrum', fontsize=18, fontweight='bold', color='#00FFCC')
    ax.set_xlabel('Time Window', fontsize=14, color='#00FFCC')
    ax.set_ylabel('Frequency', fontsize=14, color='#00FFCC')
    ax.set_zlabel('Amplitude', fontsize=14, color='#00FFCC')
    ax.tick_params(colors='#CCCCCC')
    ax.view_init(elev=35, azim=120)
    plt.tight_layout()
    plt.show()


def animate_3d_spectrum(spectrum_matrix, time, freq):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    fig.patch.set_facecolor('#181818')
    ax.set_facecolor('#181818')
    if spectrum_matrix.ndim == 1:
        spectrum_matrix = np.expand_dims(spectrum_matrix, axis=0)
    if spectrum_matrix.size == 0:
        print("Spectrum matrix is empty. Cannot animate 3D surface.")
        return
    n_windows, n_freqs = spectrum_matrix.shape
    if n_windows == 0 or n_freqs == 0:
        print("Spectrum matrix has zero dimension. Cannot animate 3D surface.")
        return
    X, Y = np.meshgrid(np.arange(n_windows), np.arange(n_freqs))
    Z = spectrum_matrix.T
    if Z.shape != X.shape:
        min_shape = (min(Z.shape[0], X.shape[0]), min(Z.shape[1], X.shape[1]))
        Z = Z[:min_shape[0], :min_shape[1]]
        X = X[:min_shape[0], :min_shape[1]]
        Y = Y[:min_shape[0], :min_shape[1]]

    def update(frame):
        ax.clear()
        ax.set_facecolor('#181818')
        ax.grid(color='#444444', linestyle='--', linewidth=0.5)
        ax.plot_wireframe(X, Y, Z, color='#00FFCC', linewidth=0.7, alpha=0.7)
        surf = ax.plot_surface(X, Y, Z, cmap=cm.cool, edgecolor='none', linewidth=0, antialiased=True, alpha=0.3)
        ax.contour(X, Y, Z, zdir='z', offset=np.min(Z)-0.2, cmap='spring', linewidths=1.2)
        ax.set_title('Quant 3D Frequency Spectrum (Animated)', fontsize=18, fontweight='bold', color='#00FFCC')
        ax.set_xlabel('Time Window', fontsize=14, color='#00FFCC')
        ax.set_ylabel('Frequency', fontsize=14, color='#00FFCC')
        ax.set_zlabel('Amplitude', fontsize=14, color='#00FFCC')
        ax.tick_params(colors='#CCCCCC')
        ax.view_init(elev=35, azim=120+frame*3)
        return surf,

    anim = FuncAnimation(fig, update, frames=80, interval=60, blit=False)
    plt.tight_layout()
    plt.show()
