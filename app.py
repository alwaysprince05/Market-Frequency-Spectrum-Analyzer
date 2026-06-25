"""
HoloQuant – Market Frequency Spectrum Analyzer
Single-page Streamlit dashboard (Streamlit 1.58 / Plotly 6.x compatible)
Author: alwaysprince05
"""

import os
import sys
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# ── Path ──────────────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Market-Frequency-Spectrum-Lab"))
from data_loader import load_data
from fft_engine import compute_fft

# ── Page config (MUST be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="HoloQuant · Spectrum Analyzer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif !important; }

/* App background */
.stApp { background: #050c18 !important; }

/* Hide default chrome */
#MainMenu, footer { visibility: hidden; }

/* Sidebar */
[data-testid="stSidebar"] > div:first-child {
    background: #070e1c !important;
    border-right: 1px solid #0d1f3c;
}
[data-testid="stSidebar"] * { color: #94a3b8 !important; }

/* Slider track */
[data-testid="stSlider"] [data-baseweb="slider"] div div div div {
    background: #00FFCC !important;
}

/* ── Hero ── */
.hero {
    padding: 32px 36px 24px;
    background: linear-gradient(120deg,#060f20 0%,#071626 50%,#050e1c 100%);
    border: 1px solid #0d2040;
    border-radius: 16px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: '';
    position: absolute;
    width: 320px; height: 320px;
    right: -80px; top: -80px;
    background: radial-gradient(circle, rgba(0,198,255,0.06) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.16em;
    color: #00c6ff;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0 0 8px;
    background: linear-gradient(90deg, #00FFCC 0%, #00c6ff 55%, #8b5cf6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
}
.hero-desc {
    font-size: 0.85rem;
    color: #334155;
    line-height: 1.6;
    max-width: 640px;
}

/* ── KPI strip ── */
.kpis {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 22px;
}
.kpi {
    background: #06101e;
    border: 1px solid #0d1f3c;
    border-radius: 12px;
    padding: 16px 18px 14px;
    position: relative;
}
.kpi::before {
    content: '';
    position: absolute;
    left: 0; top: 16px; bottom: 16px;
    width: 3px;
    border-radius: 0 2px 2px 0;
    background: linear-gradient(180deg, #00FFCC, #00c6ff);
}
.kpi-lbl {
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #1e3a5f;
    margin-bottom: 7px;
}
.kpi-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.5rem;
    font-weight: 600;
    color: #00FFCC;
}
.kpi-sub {
    font-size: 0.68rem;
    color: #1e3a5f;
    margin-top: 3px;
}

/* ── Chart card ── */
.card {
    background: #060e1c;
    border: 1px solid #0d1f3c;
    border-radius: 14px;
    padding: 18px 20px 14px;
    margin-bottom: 18px;
}
.card-hd {
    display: flex;
    align-items: center;
    gap: 9px;
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid #0d1f3c;
}
.card-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    flex-shrink: 0;
}
.card-title {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #475569;
}

/* ── Sidebar panel label ── */
.sb-hd {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #00FFCC;
    border-bottom: 1px solid #0d1f3c;
    padding-bottom: 8px;
    margin-bottom: 14px;
}

/* ── Insight box ── */
.insight {
    background: #06101e;
    border: 1px solid #0d1f3c;
    border-left: 3px solid #00FFCC;
    border-radius: 10px;
    padding: 16px;
    font-size: 0.82rem;
    color: #475569;
    line-height: 1.75;
}
.insight strong { color: #64748b; }

/* ── Footer ── */
.foot {
    text-align: center;
    padding: 20px 0 8px;
    border-top: 1px solid #0d1f3c;
    margin-top: 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    color: #1e3a5f;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sb-hd">⚙ Control Panel</div>', unsafe_allow_html=True)
    source = st.selectbox("Data Source", ["Synthetic Signal", "Yahoo Finance"])

    if source == "Yahoo Finance":
        ticker   = st.text_input("Ticker Symbol", value="BTC-USD")
        period   = st.selectbox("Period",   ["1mo","3mo","6mo","1y","2y","5y"], index=2)
        interval = st.selectbox("Interval", ["1d","1wk","1mo"], index=0)
        with st.spinner("Fetching market data…"):
            try:
                data, time = load_data(source="yfinance", ticker=ticker, period=period, interval=interval)
            except Exception:
                st.warning("Could not fetch data. Using synthetic signal.")
                data, time = load_data(source="synthetic")
                ticker = "Synthetic"
        ds_label = ticker
    else:
        data, time = load_data(source="synthetic")
        ds_label   = "Synthetic"

    st.markdown('<br><div class="sb-hd">FFT Engine</div>', unsafe_allow_html=True)

    safe_max_win = max(16, (len(data) // 2 // 16) * 16)
    window_size = st.slider("Window Size", 16, min(256, safe_max_win), min(64, safe_max_win), 16)
    step_size   = st.slider("Step / Overlap", 1, 32, 4, 1)

    st.markdown(f"""
    <div style="margin-top:20px;font-family:'JetBrains Mono',monospace;
        font-size:0.65rem;color:#1e3a5f;line-height:2;letter-spacing:0.08em;">
        SIGNAL&nbsp;&nbsp;&nbsp;{ds_label}<br>
        SAMPLES&nbsp;&nbsp;{len(data)}<br>
        WINDOW&nbsp;&nbsp;&nbsp;{window_size}<br>
        STEP&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{step_size}<br>
        ENGINE&nbsp;&nbsp;&nbsp;numpy.fft.rfft
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# COMPUTE FFT
# ══════════════════════════════════════════════════════════════════════════════
freq_full, amp_full, spectrum_matrix = compute_fft(
    data, time, window_size=window_size, step=step_size
)

price_mean = float(np.mean(data))
price_std  = float(np.std(data))
dom_idx    = int(np.argmax(amp_full)) if len(amp_full) > 0 else 0
dom_freq   = float(freq_full[dom_idx]) if dom_idx < len(freq_full) else 0.0
tot_energy = float(np.sum(amp_full ** 2))
n_windows  = spectrum_matrix.shape[0] if spectrum_matrix.ndim == 2 else 0

# ══════════════════════════════════════════════════════════════════════════════
# SHARED PLOTLY THEME
# ══════════════════════════════════════════════════════════════════════════════
BASE_LAYOUT = dict(
    template    = "plotly_dark",
    plot_bgcolor  = "rgba(0,0,0,0)",
    paper_bgcolor = "rgba(0,0,0,0)",
    margin      = dict(l=4, r=4, t=28, b=4),
    font        = dict(family="Space Grotesk, sans-serif", color="#334155", size=11),
    xaxis       = dict(gridcolor="#0d1f3c", linecolor="#0d1f3c",
                       zerolinecolor="#0d1f3c", tickfont=dict(color="#334155")),
    yaxis       = dict(gridcolor="#0d1f3c", linecolor="#0d1f3c",
                       zerolinecolor="#0d1f3c", tickfont=dict(color="#334155")),
    legend      = dict(bgcolor="rgba(0,0,0,0)", borderwidth=0,
                       font=dict(color="#475569", size=11)),
)

def neon_line(fig, x, y, color, glow_alpha, name, dash="solid"):
    """Neon glow effect: wide translucent trace + sharp foreground trace."""
    r, g, b = tuple(int(color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines",
        line=dict(color=f"rgba({r},{g},{b},{glow_alpha})", width=10),
        showlegend=False, hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines",
        line=dict(color=color, width=2, dash=dash),
        name=name,
    ))

# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero">
    <div class="hero-eyebrow">⚡ HoloQuant FFT Terminal &nbsp;·&nbsp; v2.0 &nbsp;·&nbsp; alwaysprince05</div>
    <div class="hero-title">Market Frequency<br>Spectrum Analyzer</div>
    <div class="hero-desc">
        Real-time Fast Fourier Transform decomposition of financial time-series.
        Isolate dominant cycles, detect HFT noise, and visualize spectral energy
        across sliding windows in an interactive 3-D waterfall.
        &nbsp;<span style="color:#1e3a5f">·</span>&nbsp;
        <span style="color:#00c6ff;font-family:'JetBrains Mono',monospace;font-size:0.8rem">{ds_label}</span>
        &nbsp;<span style="color:#1e3a5f">·</span>&nbsp;
        <span style="color:#334155;font-size:0.8rem">{len(data)} samples</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# KPI STRIP
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="kpis">
    <div class="kpi">
        <div class="kpi-lbl">Mean Amplitude</div>
        <div class="kpi-val">{price_mean:.2f}</div>
        <div class="kpi-sub">signal units</div>
    </div>
    <div class="kpi">
        <div class="kpi-lbl">Volatility σ</div>
        <div class="kpi-val">{price_std:.2f}</div>
        <div class="kpi-sub">std deviation</div>
    </div>
    <div class="kpi">
        <div class="kpi-lbl">Dominant Freq</div>
        <div class="kpi-val">{dom_freq:.4f}</div>
        <div class="kpi-sub">Hz (strongest cycle)</div>
    </div>
    <div class="kpi">
        <div class="kpi-lbl">Spectral Energy</div>
        <div class="kpi-val">{tot_energy:,.0f}</div>
        <div class="kpi-sub">∑ amplitude²</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ROW 1 — Time Series  +  FFT Amplitude
# ══════════════════════════════════════════════════════════════════════════════
c1, c2 = st.columns(2, gap="medium")

# ── Time series ────────────────────────────────────────────────────────
with c1:
    st.markdown("""<div class="card">
        <div class="card-hd">
            <div class="card-dot" style="background:#00FFCC;box-shadow:0 0 7px #00FFCC"></div>
            <div class="card-title">Raw Time-Series Signal</div>
        </div>""", unsafe_allow_html=True)

    fig_ts = go.Figure()
    neon_line(fig_ts, time, data, "#00FFCC", 0.08, "Amplitude")
    fig_ts.update_layout(
        **BASE_LAYOUT,
        height=300,
        xaxis_title="Sample Index",
        yaxis_title="Value",
    )
    st.plotly_chart(fig_ts, width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)

# ── FFT Spectrum ───────────────────────────────────────────────────────
with c2:
    st.markdown("""<div class="card">
        <div class="card-hd">
            <div class="card-dot" style="background:#ff007f;box-shadow:0 0 7px #ff007f"></div>
            <div class="card-title">FFT Power Spectrum</div>
        </div>""", unsafe_allow_html=True)

    fig_fft = go.Figure()
    neon_line(fig_fft, freq_full, amp_full, "#ff007f", 0.08, "Magnitude")
    if dom_freq > 0:
        fig_fft.add_vline(
            x=dom_freq,
            line=dict(color="rgba(245,158,11,0.45)", width=1, dash="dot"),
        )
        fig_fft.add_annotation(
            x=dom_freq, y=float(np.max(amp_full)) * 0.92,
            text=f"f={dom_freq:.4f}",
            showarrow=False,
            font=dict(color="#f59e0b", size=10, family="JetBrains Mono"),
        )
    fig_fft.update_layout(
        **BASE_LAYOUT,
        height=300,
        xaxis_title="Frequency (Hz)",
        yaxis_title="Magnitude",
    )
    st.plotly_chart(fig_fft, width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ROW 2 — 3-D Waterfall surface (full width)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""<div class="card">
    <div class="card-hd">
        <div class="card-dot" style="background:#8b5cf6;box-shadow:0 0 7px #8b5cf6"></div>
        <div class="card-title">Holo-Spectrum · 3-D Waterfall Surface &nbsp;
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#1e3a5f">
                (drag to rotate · scroll to zoom)
            </span>
        </div>
    </div>""", unsafe_allow_html=True)

if spectrum_matrix.ndim == 2 and spectrum_matrix.size > 0:
    Z = spectrum_matrix.T   # (n_freqs, n_windows)

    fig3d = go.Figure(data=[go.Surface(
        z=Z,
        colorscale=[
            [0.00, "#020810"],
            [0.12, "#001638"],
            [0.35, "#003080"],
            [0.60, "#0070c0"],
            [0.82, "#00c6ff"],
            [0.95, "#00FFCC"],
            [1.00, "#e0fff8"],
        ],
        lighting=dict(
            ambient=0.6, diffuse=0.85,
            specular=0.8, roughness=0.2, fresnel=0.3,
        ),
        lightposition=dict(x=150, y=250, z=200),
        colorbar=dict(
            thickness=10,
            len=0.65,
            x=1.01,
            tickfont=dict(color="#334155", size=9, family="JetBrains Mono"),
            title=dict(
                text="Energy",
                font=dict(color="#475569", size=10, family="Space Grotesk"),
                side="right",
            ),
        ),
        contours=dict(
            z=dict(show=True, usecolormap=True, highlightcolor="#00FFCC", project_z=False),
        ),
    )])

    fig3d.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=580,
        scene=dict(
            bgcolor="rgba(4,9,20,1)",
            xaxis=dict(
                title=dict(text="Time Windows",     font=dict(color="#334155", size=10)),
                gridcolor="#0d1f3c", backgroundcolor="#040916",
                showbackground=True, tickfont=dict(color="#1e3a5f", size=8),
            ),
            yaxis=dict(
                title=dict(text="Frequency Bins",   font=dict(color="#334155", size=10)),
                gridcolor="#0d1f3c", backgroundcolor="#040916",
                showbackground=True, tickfont=dict(color="#1e3a5f", size=8),
            ),
            zaxis=dict(
                title=dict(text="Amplitude",        font=dict(color="#334155", size=10)),
                gridcolor="#0d1f3c", backgroundcolor="#040916",
                showbackground=True, tickfont=dict(color="#1e3a5f", size=8),
            ),
            camera=dict(eye=dict(x=1.55, y=1.55, z=0.95)),
            aspectmode="auto",
        ),
    )
    st.plotly_chart(fig3d, width="stretch")
else:
    st.error("⚠️  Spectrum matrix is empty — reduce Window Size or pick a longer data period.")

st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ROW 3 — Trading Simulation + Insight panel
# ══════════════════════════════════════════════════════════════════════════════
c3, c4 = st.columns([3, 1], gap="medium")

with c3:
    st.markdown("""<div class="card">
        <div class="card-hd">
            <div class="card-dot" style="background:#4facfe;box-shadow:0 0 7px #4facfe"></div>
            <div class="card-title">Live Multi-Line Trading Simulation</div>
        </div>""", unsafe_allow_html=True)

    n   = 160
    t   = np.arange(n)
    rng = np.random.default_rng(42)
    base  = np.cumsum(rng.standard_normal(n)) + 130
    upper = base + np.abs(np.sin(t / 14)) * 7 + rng.standard_normal(n) * 0.6
    lower = base - np.abs(np.cos(t / 20)) * 6 + rng.standard_normal(n) * 0.6
    vol   = np.abs(rng.standard_normal(n)) * 28

    fig_trade = go.Figure()

    # Volume bars (background y2)
    fig_trade.add_trace(go.Bar(
        x=t, y=vol,
        marker_color="rgba(79,172,254,0.07)",
        name="Volume", yaxis="y2", showlegend=False,
    ))

    # Channel fill
    fig_trade.add_trace(go.Scatter(
        x=np.concatenate([t, t[::-1]]),
        y=np.concatenate([upper, lower[::-1]]),
        fill="toself", fillcolor="rgba(0,255,204,0.04)",
        line=dict(color="rgba(0,0,0,0)"),
        showlegend=False, hoverinfo="skip",
    ))

    neon_line(fig_trade, t, upper, "#4facfe", 0.07, "Upper Band", dash="dash")
    neon_line(fig_trade, t, lower, "#ff007f", 0.07, "Lower Band", dash="dash")
    neon_line(fig_trade, t, base,  "#00FFCC", 0.09, "Signal")

    fig_trade.update_layout(
        **BASE_LAYOUT,
        height=340,
        xaxis_title="Time Steps",
        yaxis_title="Price Level",
        yaxis2=dict(
            overlaying="y", side="right",
            showgrid=False, showticklabels=False,
            range=[0, float(vol.max()) * 5],
        ),
    )
    st.plotly_chart(fig_trade, width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div style="height:8px"></div>
    <div class="insight">
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
             letter-spacing:0.14em;color:#00FFCC;text-transform:uppercase;margin-bottom:14px;">
            📡 Signal Insights
        </div>
        <strong>Source</strong><br>
        <span style="font-family:'JetBrains Mono',monospace;color:#00c6ff;font-size:0.82rem">
            {ds_label}
        </span><br><br>
        <strong>Dominant Frequency</strong><br>
        <span style="font-family:'JetBrains Mono',monospace;color:#00c6ff;font-size:0.82rem">
            {dom_freq:.5f} Hz
        </span><br><br>
        <strong>Std Deviation σ</strong><br>
        <span style="font-family:'JetBrains Mono',monospace;color:#00c6ff;font-size:0.82rem">
            {price_std:.4f}
        </span><br><br>
        <strong>Spectral Windows</strong><br>
        <span style="font-family:'JetBrains Mono',monospace;color:#00c6ff;font-size:0.82rem">
            {n_windows}
        </span><br><br>
        <strong>Total Energy</strong><br>
        <span style="font-family:'JetBrains Mono',monospace;color:#00c6ff;font-size:0.82rem">
            {tot_energy:,.0f}
        </span>
        <div style="margin-top:16px;font-size:0.75rem;color:#1e3a5f;line-height:1.7;">
            High energy at <em>low</em> frequencies → macro trend.<br>
            High energy at <em>high</em> frequencies → noise or HFT.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="foot">
    HoloQuant Spectrum Analyzer &nbsp;·&nbsp;
    github.com/alwaysprince05/Market-Frequency-Spectrum-Analyzer &nbsp;·&nbsp;
    Powered by numpy.fft &amp; Streamlit
</div>
""", unsafe_allow_html=True)
