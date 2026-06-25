import os
import sys
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Add Market-Frequency-Spectrum-Lab to sys.path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'Market-Frequency-Spectrum-Lab'))

from data_loader import load_data
from fft_engine import compute_fft

# Page configuration
st.set_page_config(
    page_title="HoloQuant Spectrum Analyzer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling (Cyberpunk/Quant Neon Theme)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Space+Grotesk:wght@400;700&display=swap');

    /* Global styling overrides */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0d1224 0%, #05070f 100%);
        font-family: 'Outfit', sans-serif;
        color: #e2e8f0;
    }
    
    /* Title banner styling */
    .title-banner {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.6) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 242, 254, 0.15);
        border-radius: 16px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        text-align: center;
    }
    
    .glowing-title {
        background: linear-gradient(90deg, #00FFCC 0%, #00f2fe 50%, #7f00ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800;
        font-size: 3rem;
        margin: 0;
        letter-spacing: -1px;
        filter: drop-shadow(0 2px 8px rgba(0, 242, 254, 0.3));
    }
    
    .subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 300;
        margin-top: 10px;
    }

    /* Sidebar customization */
    div[data-testid="stSidebar"] {
        background-color: #060913;
        border-right: 1px solid rgba(0, 242, 254, 0.1);
    }
    
    /* Custom Card container */
    .quant-card {
        background: rgba(13, 20, 38, 0.6);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 2px solid #00f2fe;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .quant-card:hover {
        border-top: 2px solid #00FFCC;
        box-shadow: 0 10px 30px rgba(0, 242, 254, 0.15);
        transform: translateY(-2px);
    }

    /* Custom KPI Cards */
    .kpi-container {
        display: flex;
        gap: 15px;
        margin-bottom: 25px;
    }
    .kpi-box {
        flex: 1;
        background: rgba(15, 23, 42, 0.55);
        border: 1px solid rgba(0, 255, 204, 0.1);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: inset 0 0 10px rgba(0, 255, 204, 0.02);
    }
    .kpi-val {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #00FFCC;
        margin: 5px 0 0 0;
        text-shadow: 0 0 10px rgba(0, 255, 204, 0.3);
    }
    .kpi-label {
        font-size: 0.8rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Widgets labels styling */
    .stSlider label, .stSelectbox label, .stTextInput label {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Title Banner
st.markdown("""
    <div class="title-banner">
        <h1 class="glowing-title">⚡ HOLOQUANT SPECTRUM ANALYZER</h1>
        <div class="subtitle">Next-Generation Fast Fourier Transform (FFT) Terminal for Algorithmic & High-Frequency Signal Analysis</div>
    </div>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.markdown("<h2 style='color:#00FFCC; font-family:\"Space Grotesk\", sans-serif; font-size:1.5rem; border-bottom:1px solid rgba(0, 242, 254, 0.2); padding-bottom: 10px;'>⚙️ CONTROL PANEL</h2>", unsafe_allow_html=True)
source = st.sidebar.selectbox("Market Source", ["Synthetic Generator", "Yahoo Finance (yfinance)"])

if source == "Yahoo Finance (yfinance)":
    ticker = st.sidebar.text_input("Ticker / Symbol", value="BTC-USD")
    period = st.sidebar.selectbox("Time Horizon", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"], index=1)
    interval = st.sidebar.selectbox("Data Resolution", ["1d", "1wk", "1mo"], index=0)
    data, time = load_data(source='yfinance', ticker=ticker, period=period, interval=interval)
else:
    st.sidebar.markdown("<div style='background:rgba(0, 255, 204, 0.05); border:1px solid rgba(0, 255, 204, 0.2); border-radius:8px; padding:10px; color:#00FFCC; font-size:0.85rem; margin-bottom:15px;'>🔬 Generating multi-frequency synth signal + Gaussian distribution noise.</div>", unsafe_allow_html=True)
    data, time = load_data(source='synthetic')

# FFT Parameters
st.sidebar.markdown("<h3 style='color:#00f2fe; font-size:1.1rem; margin-top:20px;'>FFT Transform Engine</h3>", unsafe_allow_html=True)
window_size = st.sidebar.slider("Spectral Window Size", min_value=16, max_value=256, value=64, step=16)
step = st.sidebar.slider("Engine Overlap (Step)", min_value=1, max_value=32, value=4, step=1)

# Safety check
if window_size >= len(data):
    st.sidebar.warning(f"Window size ({window_size}) adjusted for limited data size.")
    window_size = min(32, len(data) // 2)

# Compute FFT
freq_full, amplitude_full, spectrum_matrix = compute_fft(data, time, window_size=window_size, step=step)

# Key Metrics Calculation
price_mean = np.mean(data)
price_std = np.std(data)
max_amp_idx = np.argmax(amplitude_full)
dominant_freq = freq_full[max_amp_idx] if max_amp_idx < len(freq_full) else 0.0
total_energy = np.sum(amplitude_full**2)

# Display KPI Block
st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-box">
            <div class="kpi-label">Average Amplitude / Price</div>
            <div class="kpi-val">{price_mean:.2f}</div>
        </div>
        <div class="kpi-box">
            <div class="kpi-label">Standard Deviation</div>
            <div class="kpi-val">{price_std:.2f}</div>
        </div>
        <div class="kpi-box">
            <div class="kpi-label">Dominant Frequency</div>
            <div class="kpi-val">{dominant_freq:.4f} Hz</div>
        </div>
        <div class="kpi-box">
            <div class="kpi-label">Total Spectral Energy</div>
            <div class="kpi-val">{total_energy:.1f}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Layout: Main Plots
col_left, col_right = st.columns(2)

with col_left:
    st.markdown('<div class="quant-card"><h3>📈 Raw Time Series Signal</h3>', unsafe_allow_html=True)
    fig_time = go.Figure()
    # Glowing effect using double lines
    fig_time.add_trace(go.Scatter(
        x=time, y=data,
        mode='lines',
        line=dict(color='rgba(0, 242, 254, 0.2)', width=6),
        hoverinfo='none',
        showlegend=False
    ))
    fig_time.add_trace(go.Scatter(
        x=time, y=data,
        mode='lines',
        line=dict(color='#00f2fe', width=2),
        name='Price/Value'
    ))
    fig_time.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(title="Time Offset / Index", gridcolor="#1e293b", linecolor="#1e293b"),
        yaxis=dict(title="Price Unit", gridcolor="#1e293b", linecolor="#1e293b"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_time, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="quant-card"><h3>⚡ Spectral Power (FFT Amplitude)</h3>', unsafe_allow_html=True)
    fig_freq = go.Figure()
    # Glowing effect
    fig_freq.add_trace(go.Scatter(
        x=freq_full, y=amplitude_full,
        mode='lines',
        line=dict(color='rgba(255, 0, 127, 0.2)', width=6),
        hoverinfo='none',
        showlegend=False
    ))
    fig_freq.add_trace(go.Scatter(
        x=freq_full, y=amplitude_full,
        mode='lines',
        line=dict(color='#ff007f', width=2),
        name='Spectral Amplitude'
    ))
    fig_freq.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(title="Frequency Component (Hz)", gridcolor="#1e293b", linecolor="#1e293b"),
        yaxis=dict(title="Relative Strength", gridcolor="#1e293b", linecolor="#1e293b"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_freq, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 3D surface plot section
st.markdown('<div class="quant-card"><h3>🌌 Holo-Spectrum 3D Waterfall Surface</h3>', unsafe_allow_html=True)

if spectrum_matrix.size > 0:
    n_windows, n_freqs = spectrum_matrix.shape
    X, Y = np.meshgrid(np.arange(n_windows), np.arange(n_freqs))
    Z = spectrum_matrix.T

    # Premium custom color gradient mimicking glowing spectrum surfaces
    custom_colorscale = [
        [0.0, '#0d0d26'],     # Background deep space blue
        [0.1, '#0052d4'],     # Electric indigo
        [0.5, '#4364f7'],     # Cyber blue
        [0.85, '#00f2fe'],    # Bright cyan
        [1.0, '#00FFCC']      # Radioactive green
    ]

    fig_3d = go.Figure(data=[go.Surface(
        z=Z,
        x=X,
        y=Y,
        colorscale=custom_colorscale,
        lighting=dict(
            ambient=0.5,
            diffuse=0.9,
            specular=1.5,
            roughness=0.08,
            fresnel=0.5
        ),
        lightposition=dict(x=100, y=200, z=150),
        colorbar=dict(
            title="Strength",
            titleside="top",
            tickcolor="#e2e8f0",
            titlefont=dict(color="#e2e8f0", size=12),
            tickfont=dict(color="#94a3b8", size=10)
        )
    )])

    fig_3d.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        scene=dict(
            xaxis=dict(
                title="Sliding Window Index",
                gridcolor="#1e293b",
                backgroundcolor="rgba(10, 15, 30, 0.5)",
                showbackground=True
            ),
            yaxis=dict(
                title="Frequency Component",
                gridcolor="#1e293b",
                backgroundcolor="rgba(10, 15, 30, 0.5)",
                showbackground=True
            ),
            zaxis=dict(
                title="Energy Density",
                gridcolor="#1e293b",
                backgroundcolor="rgba(10, 15, 30, 0.5)",
                showbackground=True
            ),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.2)
            ),
            bgcolor="rgba(0,0,0,0)"
        ),
        height=700
    )
    st.plotly_chart(fig_3d, use_container_width=True)
else:
    st.error("Spectrum matrix contains zero elements. Please adjust settings.")
st.markdown('</div>', unsafe_allow_html=True)


# Bottom section: Animated Trading Simulation Overlay
st.markdown('<div class="quant-card"><h3>🎬 Live Trading Spectrum Mockup (Animated Sim)</h3>', unsafe_allow_html=True)
col_left_s, col_right_s = st.columns([3, 1])

with col_left_s:
    steps_ani = 120
    x_ani = np.arange(steps_ani)
    np.random.seed(42)
    price_ani = np.cumsum(np.random.randn(steps_ani)) + 150
    line2_ani = price_ani + np.sin(x_ani / 5) * 5 + np.random.randn(steps_ani) * 2
    line3_ani = price_ani - np.cos(x_ani / 10) * 8 + np.random.randn(steps_ani) * 1.5

    fig_ani = go.Figure()
    fig_ani.add_trace(go.Scatter(x=x_ani, y=price_ani, name="Signal (Close)", line=dict(color="#00FFCC", width=2.5)))
    fig_ani.add_trace(go.Scatter(x=x_ani, y=line2_ani, name="HFT High Channel", line=dict(color="#00f2fe", width=1, dash="dash")))
    fig_ani.add_trace(go.Scatter(x=x_ani, y=line3_ani, name="HFT Low Channel", line=dict(color="#ff007f", width=1, dash="dot")))

    fig_ani.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(gridcolor="#1e293b", linecolor="#1e293b"),
        yaxis=dict(gridcolor="#1e293b", linecolor="#1e293b"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_ani, use_container_width=True)

with col_right_s:
    st.markdown("""
        <div style='padding-top:15px;'>
            <h4 style='color:#00FFCC;'>💡 Analysis Insights</h4>
            <p style='font-size:0.9rem; color:#94a3b8; line-height:1.5;'>
                This model simulates a Fourier analysis window traversing across incoming trade ticks. 
                By isolating distinct spectral modes, high-frequency anomalies and cyclical signals can be detected before they manifest in simple trend-line averages.
            </p>
            <p style='font-size:0.85rem; color:#64748b; font-style:italic;'>
                Use the Control Panel on the left to change symbols or resolutions.
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
