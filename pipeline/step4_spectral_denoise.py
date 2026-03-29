import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def butter_lowpass_filter(data, cutoff, fs, order=5):
    """
    Applies a Butterworth low-pass filter to the data.
    """
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

def apply_spectral_denoising(df, columns, order=4, cutoff=0.1):
    """
    Step 4: Removes high-frequency noise from telemetry signals using 
    a Butterworth low-pass filter. Zero-phase filtering ensures 
    no time-shift in telemetry data.
    """
    df_clean = df.copy()
    fs = 1.0  # Sampling frequency (assumed 1 Hz for this telemetry stream)
    
    for col in columns:
        if col not in df_clean.columns:
            continue
            
        try:
            # Drop NaN values for filtering, then re-index
            original_series = df_clean[col].ffill().bfill()
            filtered_signal = butter_lowpass_filter(original_series.values, cutoff, fs, order)
            df_clean[col] = filtered_signal
        except Exception as e:
            logging.error(f"Error filtering column {col}: {e}")
            
    logging.info(f"[Step 4: Spectral] Applied Butterworth Low-Pass (Order={order}, Cutoff={cutoff}) to {len(columns)} columns.")
    return df_clean

if __name__ == "__main__":
    # Test block
    data = pd.DataFrame({'val': np.sin(np.linspace(0, 10, 100)) + np.random.normal(0, 0.5, 100)})
    cleaned = apply_spectral_denoising(data, ['val'])
    print(cleaned.head())
