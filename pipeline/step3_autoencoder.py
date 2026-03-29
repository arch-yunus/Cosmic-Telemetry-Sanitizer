import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def check_contextual_anomalies(df, columns=['battery_voltage', 'bus_current', 'temp_celsius', 'rw_speed_rpm', 'sun_sensor_lux']):
    """
    Uses Isolation Forest to detect multivariate/contextual anomalies 
    that univariate filters (MAD) might miss.
    """
    logging.info("[Step 3: AI] Initiating multivariate isolation forest analysis...")
    
    # Select features for AI analysis
    data = df[columns].ffill().bfill()
    
    # Initialize and fit Isolation Forest
    # contamination defines the expected proportion of outliers in the data
    model = IsolationForest(contamination=0.02, random_state=42)
    predictions = model.fit_predict(data)
    
    # predictions: -1 for anomaly, 1 for normal
    anomalies_mask = (predictions == -1)
    anomalies_count = anomalies_mask.sum()
    
    # For contextual anomalies, we might not want to just replace with median,
    # but for this prototype, we will mark them and perform a local smoothing.
    if anomalies_count > 0:
        for col in columns:
            # Simple fix: Replace with rolling mean for the AI-detected weird blocks
            rolling_mean = df[col].rolling(window=10, center=True).mean().ffill().bfill()
            df.loc[anomalies_mask, col] = rolling_mean[anomalies_mask]
            
    logging.info(f"[Step 3: AI] Detected {anomalies_count} contextual anomalies (correlation violations).")
    return df

if __name__ == "__main__":
    df = pd.read_csv("data/raw_telemetry/sample_orbit_data.csv")
    df = check_contextual_anomalies(df)
