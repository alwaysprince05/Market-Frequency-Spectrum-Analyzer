# data_loader.py
import numpy as np

def load_data(source='synthetic', ticker=None, period=None, interval=None):
    if source == 'yfinance':
        try:
            import yfinance as yf
            df = yf.download(ticker, period=period, interval=interval)
            data = df['Close'].values
            time = np.arange(len(data))
            return data, time
        except Exception as e:
            print(f"yfinance error: {e}. Using synthetic data.")
    # Synthetic signal: sum of sinusoids + noise
    n = 256
    time = np.linspace(0, 10, n)
    data = (
        np.sin(2 * np.pi * 1 * time) +
        0.5 * np.sin(2 * np.pi * 3 * time) +
        0.2 * np.sin(2 * np.pi * 7 * time) +
        np.random.normal(0, 0.2, n)
    )
    return data, time
