# Market-Frequency-Spectrum-Lab

Analyze financial time series using Fast Fourier Transform and visualize the frequency spectrum in 3D.

## Features
- Load financial price data (yfinance) or generate synthetic signals
- Apply FFT to convert time series to frequency components
- Compute frequency intensity values
- Visualize results as a 3D frequency spectrum surface (X=time window, Y=frequency, Z=amplitude)
- Render colorful 3D surface plots
- Animation showing spectrum evolving over time
- Additional 2D plots: original price signal, frequency spectrum
- Scientific signal-processing graphics with color gradients

## Project Structure
```
Market-Frequency-Spectrum-Lab/
  main.py
  data_loader.py
  fft_engine.py
  visualization.py
  requirements.txt
  README.md
```

## Installation
1. Install Python 3.8+
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
Run the main script:
```
python main.py
```

## Notes
- For real market data, ensure internet access and yfinance installed.
- For synthetic data, no external API is needed.
- Visualizations use matplotlib 3D. For interactive plots, you can extend with Plotly.
