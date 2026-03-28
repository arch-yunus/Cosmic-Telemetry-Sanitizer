import numpy as np
import pandas as pd

def apply_mad_filter(df, column, window=5, threshold=3):
    """
    Applies Median Absolute Deviation (MAD) filter to remove spikes.
    """
    df_clean = df.copy()
    rolling_median = df_clean[column].rolling(window=window, center=True).median()
    rolling_mad = (df_clean[column] - rolling_median).abs().rolling(window=window, center=True).median()
    
    # Calculate Z-score based on MAD
    z_score = 0.6745 * (df_clean[column] - rolling_median) / rolling_mad
    
    # Detect outliers
    outliers = z_score.abs() > threshold
    
    # Replace outliers with rolling median
    df_clean.loc[outliers, column] = rolling_median[outliers]
    
    print(f"[MAD Filter] Processed {column}: Detected and removed {outliers.sum()} spikes.")
    return df_clean

if __name__ == "__main__":
    # Test logic
    data = {'val': [10, 11, 100, 10, 11]}
    df = pd.DataFrame(data)
    df_filtered = apply_mad_filter(df, 'val')
    print(df_filtered)
