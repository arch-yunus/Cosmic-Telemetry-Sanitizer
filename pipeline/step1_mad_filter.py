import numpy as np
import pandas as pd

def apply_mad_filter(df, columns, window=15, threshold=3.5):
    """
    Advanced MAD filter with support for multiple columns and adaptive handling.
    """
    df_clean = df.copy()
    anomalies_count = 0
    
    for col in columns:
        if col not in df_clean.columns: continue
        
        # Calculate rolling median and MAD
        rolling_median = df_clean[col].rolling(window=window, center=True).median()
        # Fill NaNs at edges with the closest median value
        rolling_median = rolling_median.ffill().bfill()
        
        abs_deviation = (df_clean[col] - rolling_median).abs()
        mad = abs_deviation.rolling(window=window, center=True).median()
        mad = mad.ffill().bfill()
        
        # Prevent division by zero
        mad = mad.replace(0, 1e-6)
        
        # Calculate Modified Z-score
        z_score = 0.6745 * (df_clean[col] - rolling_median) / mad
        
        # Detect outliers
        outliers = z_score.abs() > threshold
        anomalies_count += outliers.sum()
        
        # Replace outliers with rolling median (Imputation)
        df_clean.loc[outliers, col] = rolling_median[outliers]
        
    print(f"[Step 1: MAD] Scanned {len(columns)} columns. Found and mitigated {anomalies_count} point anomalies.")
    return df_clean

if __name__ == "__main__":
    df = pd.read_csv("data/raw_telemetry/sample_orbit_data.csv")
    cols = ['battery_voltage', 'temp_celsius', 'rw_speed_rpm']
    df_filtered = apply_mad_filter(df, cols)
