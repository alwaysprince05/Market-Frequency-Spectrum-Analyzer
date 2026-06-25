import os
import sys
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# ── Path setup ────────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Market-Frequency-Spectrum-Lab"))
from data_loader import load_data
from fft_engine import compute_fft

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HoloQuant · Spectrum Analyzer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
}
.stApp {
    background: #060a14;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #08101f !important;
    border-right: 1px solid #0f2040;
}
[data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stTextInput label {
    font-size: 0.78rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #4facfe !important;
}

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #040d1e 0%, #071428 60%, #09193a 100%);
    border: 1px solid #0f2a50;
    border-radius: 18px;
    padding: 36px 40px 28px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(0,242,254,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    margin: 0 0 6px;
    background: linear-gradient(90deg, #00FFCC 0%, #00c6ff 50%, #9b59b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}
.hero-sub {
    color: #475569;
    font-size: 0.9rem;
    font-weight: 400;
    letter-spacing: 0.02em;
}
.hero-badge {
    display: inline-block;
    background: rgba(0,242,254,0.08);
    border: 1px solid rgba(0,242,254,0.2);
    color: #00f2fe;
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.1em;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 14px;
}

/* ── KPI strip ── */
.kpi-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 26px;
}
.kpi-card {
    background: #08111f;
    border: 1px solid #0f2040;
    border-radius: 12px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00FFCC, #00c6ff);
    border-radius: 0 0 12px 12px;
}
.kpi-label {
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #334155;
    margin-bottom: 8px;
}
.kpi-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.65rem;
    font-weight: 600;
    color: #00FFCC;
    text-shadow: 0 0 20px rgba(0,255,204,0.25);
}
.kpi-unit {
    font-size: 0.75rem;
    color: #334155;
    margin-top: 4px;
}

/* ── Section headers ── */
.section-head {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
    border-bottom: 1px solid #0f2040;
    padding-bottom: 10px;
}
.section-head-title {
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #94a3b8;
}
.section-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #00FFCC;
    box-shadow: 0 0 8px #00FFCC;
    flex-shrink: 0;
}

/* ── Chart wrapper ── */
.chart-box {
    background: #07101f;
    border: 1px solid #0f2040;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 20px;
}

/* ── Sidebar panel header ── */
.panel-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #00FFCC;
    border-bottom: 1px solid #0f2040;
    padding-bottom: 10px;
    margin-bottom: 16px;
}

/* ── Insight card ── */
.insight-card {
    background: #08111f;
    border: 1px solid #0f2040;
    border-left: 3px solid #00FFCC;
    border-radius: 10px;
    padding: 16px 18px;
    font-size: 0.85rem;
    color: #64748b;
    line-height: 1.7;
}
.insight-card b {
    color: #94a3b8;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #060a14; }
::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="panel-header">⚙ Control Panel</div>', unsafe_allow_html=True)

    source = st.selectbox("Data Source", ["Synthetic Signal", "Yahoo Finance"])

    if source == "Yahoo Finance":
        ticker   = st.text_input("Ticker Symbol", value="BTC-USD")
        period   = st.selectbox("Period",   ["1mo","3mo","6mo","1y","2y","5y"], index=2)
        interval = st.selectbox("Interval", ["1d","1wk","1mo"], index=0)
        data, time = load_data(source="yfinance", ticker=ticker, period=period, interval=interval)
        ds_label = ticker
    else:
        data, time = load_data(source="synthetic")
        ds_label = "Synthetic"

    st.markdown("---")
    st.markdown('<div class="panel-header">FFT Engine</div>', unsafe_allow_html=True)
    window_size = st.slider("Window Size",  min_value=16, max_value=256, value=64,  step=16)
    step_size   = st.slider("Step / Overlap", min_value=1,  max_value=32,  value=4,   step=1)

    if window_size >= len(data):
        st.warning(f"Window ({window_size}) ≥ data length ({len(data)}). Auto-adjusted.")
        window_size = max(16, len(data) // 4)

    st.markdown("---")
    st.markdown(f"<div style='font-size:0.7rem;color:#1e3a5f;font-family:JetBrains Mono,monospace;'>SIGNAL: {ds_label}<br>SAMPLES: {len(data)}<br>ENGINE: numpy.fft.rfft</div>", unsafe_allow_html=True)

# ── COMPUTE ───────────────────────────────────────────────────────────────────
freq_full, amp_full, spectrum_matrix = compute_fft(data, time, window_size=window_size, step=step_size)

price_mean = float(np.mean(data))
price_std  = float(np.std(data))
dom_idx    = int(np.argmax(amp_full))
dom_freq   = float(freq_full[dom_idx]) if dom_idx < len(freq_full) else 0.0
tot_energy = float(np.sum(amp_full ** 2))

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-badge">⚡ HOLOQUANT · FFT TERMINAL v2.0</div>
    <div class="hero-title">Market Frequency Spectrum Analyzer</div>
    <div class="hero-sub">
        Real-time Fast Fourier Transform signal decomposition &amp; 3D spectral waterfall visualization
        &nbsp;·&nbsp; Data Source: <strong style="color:#4facfe">{ds_label}</strong>
        &nbsp;·&nbsp; Samples: <strong style="color:#4facfe">{len(data)}</strong>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI STRIP ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="kpi-strip">
    <div class="kpi-card">
        <div class="kpi-label">Mean Amplitude</div>
        <div class="kpi-value">{price_mean:.2f}</div>
        <div class="kpi-unit">signal units</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Std Deviation</div>
        <div class="kpi-value">{price_std:.2f}</div>
        <div class="kpi-unit">σ volatility</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Dominant Freq</div>
        <div class="kpi-value">{dom_freq:.4f}</div>
        <div class="kpi-unit">Hz</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Spectral Energy</div>
        <div class="kpi-value">{tot_energy:,.0f}</div>
        <div class="kpi-unit">∑ amplitude²</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── PLOT HELPERS ──────────────────────────────────────────────────────────────
DARK_LAYOUT = dict(
    template="plotly_dark",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=0, t=30, b=0),
    font=dict(family="Space Grotesk, sans-serif", color="#64748b", size=11),
    xaxis=dict(gridcolor="#0f2040", linecolor="#0f2040", zerolinecolor="#0f2040"),
    yaxis=dict(gridcolor="#0f2040", linecolor="#0f2040", zerolinecolor="#0f2040"),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)"),
)

def glow_line(fig, x, y, color_solid, color_glow, name):
    """Add a neon line with a wide translucent glow behind it."""
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines",
        line=dict(color=color_glow, width=8),
        showlegend=False, hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines",
        line=dict(color=color_solid, width=2),
        name=name,
    ))

# ── ROW 1: Time series + FFT Spectrum ─────────────────────────────────────────
col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown('<div class="chart-box"><div class="section-head"><div class="section-dot"></div><div class="section-head-title">Raw Time-Series Signal</div></div>', unsafe_allow_html=True)
    fig1 = go.Figure()
    glow_line(fig1, time, data, "#00FFCC", "rgba(0,255,204,0.12)", "Price / Value")
    fig1.update_layout(
        **DARK_LAYOUT,
        height=320,
        xaxis_title="Sample Index",
        yaxis_title="Amplitude",
    )
    st.plotly_chart(fig1, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-box"><div class="section-head"><div class="section-dot" style="background:#ff007f;box-shadow:0 0 8px #ff007f"></div><div class="section-head-title">FFT Power Spectrum (Amplitude)</div></div>', unsafe_allow_html=True)
    fig2 = go.Figure()
    glow_line(fig2, freq_full, amp_full, "#ff007f", "rgba(255,0,127,0.12)", "Spectral Amplitude")
    # Mark dominant frequency
    fig2.add_vline(
        x=dom_freq,
        line=dict(color="rgba(255,165,0,0.5)", width=1, dash="dot"),
        annotation=dict(text=f"  f={dom_freq:.3f}Hz", font=dict(color="#f59e0b", size=10)),
        annotation_position="top left",
    )
    fig2.update_layout(
        **DARK_LAYOUT,
        height=320,
        xaxis_title="Frequency (Hz)",
        yaxis_title="Magnitude",
    )
    st.plotly_chart(fig2, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

# ── ROW 2: 3-D Waterfall ──────────────────────────────────────────────────────
st.markdown('<div class="chart-box"><div class="section-head"><div class="section-dot" style="background:#9b59b6;box-shadow:0 0 8px #9b59b6"></div><div class="section-head-title">Holo-Spectrum · 3D Waterfall Surface</div></div>', unsafe_allow_html=True)

if spectrum_matrix.ndim == 2 and spectrum_matrix.size > 0:
    Z = spectrum_matrix.T          # shape: (n_freqs, n_windows)

    colorscale = [
        [0.00, "#04080f"],
        [0.15, "#001a4d"],
        [0.40, "#0052d4"],
        [0.70, "#00c6ff"],
        [0.90, "#00FFCC"],
        [1.00, "#ffffff"],
    ]

    fig3d = go.Figure(data=[go.Surface(
        z=Z,
        colorscale=colorscale,
        lighting=dict(ambient=0.55, diffuse=0.85, specular=0.9, roughness=0.15, fresnel=0.4),
        lightposition=dict(x=100, y=200, z=150),
        colorbar=dict(
            thickness=12,
            len=0.7,
            tickfont=dict(color="#475569", size=10, family="JetBrains Mono"),
            title=dict(text="Energy", font=dict(color="#64748b", size=11)),
        ),
    )])

    fig3d.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=620,
        scene=dict(
            bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                title=dict(text="Time Windows", font=dict(color="#475569", size=11)),
                gridcolor="#0f2040",
                backgroundcolor="#06090f",
                showbackground=True,
                tickfont=dict(color="#334155", size=9),
            ),
            yaxis=dict(
                title=dict(text="Frequency Bins", font=dict(color="#475569", size=11)),
                gridcolor="#0f2040",
                backgroundcolor="#06090f",
                showbackground=True,
                tickfont=dict(color="#334155", size=9),
            ),
            zaxis=dict(
                title=dict(text="Amplitude", font=dict(color="#475569", size=11)),
                gridcolor="#0f2040",
                backgroundcolor="#06090f",
                showbackground=True,
                tickfont=dict(color="#334155", size=9),
            ),
            camera=dict(eye=dict(x=1.6, y=1.6, z=1.0)),
        ),
    )
    st.plotly_chart(fig3d, width="stretch")
else:
    st.error("⚠️ Spectrum matrix is empty. Reduce Window Size or choose a larger data period.")

st.markdown('</div>', unsafe_allow_html=True)

# ── ROW 3: Trading Sim + Insight ──────────────────────────────────────────────
col3, col4 = st.columns([3, 1], gap="medium")

with col3:
    st.markdown('<div class="chart-box"><div class="section-head"><div class="section-dot" style="background:#4facfe;box-shadow:0 0 8px #4facfe"></div><div class="section-head-title">Live Multi-Line Trading Simulation</div></div>', unsafe_allow_html=True)

    n = 150
    t = np.arange(n)
    rng = np.random.default_rng(42)
    base   = np.cumsum(rng.standard_normal(n)) + 120
    upper  = base + np.abs(np.sin(t / 12)) * 6 + rng.standard_normal(n) * 0.8
    lower  = base - np.abs(np.cos(t / 18)) * 7 + rng.standard_normal(n) * 0.8
    volume = np.abs(rng.standard_normal(n)) * 30

    fig4 = go.Figure()

    # Volume bars in background
    fig4.add_trace(go.Bar(
        x=t, y=volume,
        marker_color="rgba(79,172,254,0.08)",
        name="Volume",
        yaxis="y2",
        showlegend=False,
    ))

    # Glow fills between channels
    fig4.add_trace(go.Scatter(
        x=np.concatenate([t, t[::-1]]),
        y=np.concatenate([upper, lower[::-1]]),
        fill="toself",
        fillcolor="rgba(0,255,204,0.04)",
        line=dict(color="rgba(0,0,0,0)"),
        showlegend=False, hoverinfo="skip",
    ))

    # Lines
    glow_line(fig4, t, base,  "#00FFCC", "rgba(0,255,204,0.10)", "Signal")
    glow_line(fig4, t, upper, "#4facfe", "rgba(79,172,254,0.08)", "Upper Band")
    glow_line(fig4, t, lower, "#ff007f", "rgba(255,0,127,0.08)",  "Lower Band")

    fig4.update_layout(
        **DARK_LAYOUT,
        height=340,
        xaxis_title="Time Steps",
        yaxis_title="Price Level",
        yaxis2=dict(
            overlaying="y", side="right",
            showgrid=False, showticklabels=False, range=[0, volume.max() * 4],
        ),
    )
    st.plotly_chart(fig4, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="height:14px"></div>
    <div class="insight-card">
        <div style="font-size:0.7rem;letter-spacing:0.12em;text-transform:uppercase;color:#00FFCC;margin-bottom:12px;">📡 Signal Insights</div>
        <b>Dominant Frequency:</b><br>
        <span style="font-family:'JetBrains Mono',monospace;color:#4facfe">{dom_freq:.5f} Hz</span><br><br>
        <b>Volatility (σ):</b><br>
        <span style="font-family:'JetBrains Mono',monospace;color:#4facfe">{price_std:.4f}</span><br><br>
        <b>Spectral Energy:</b><br>
        <span style="font-family:'JetBrains Mono',monospace;color:#4facfe">{tot_energy:,.1f}</span><br><br>
        <b>FFT Windows:</b><br>
        <span style="font-family:'JetBrains Mono',monospace;color:#4facfe">{spectrum_matrix.shape[0] if spectrum_matrix.ndim==2 else 0}</span><br><br>
        <div style="margin-top:14px;font-size:0.75rem;color:#1e3a5f;line-height:1.6;">
            Frequency decomposition isolates cyclical patterns invisible in raw price series. 
            High spectral energy at low frequencies signals trend; at high frequencies, noise or HFT activity.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:30px;padding:20px;border-top:1px solid #0f2040;">
    <span style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#1e3a5f;letter-spacing:0.12em;">
        HOLOQUANT SPECTRUM ANALYZER &nbsp;·&nbsp; github.com/alwaysprince05 &nbsp;·&nbsp; FFT ENGINE: numpy.fft
    </span>
</div>
""", unsafe_allow_html=True)
