import numpy as np
import pandas as pd

class AdaptiveKalman:
    def __init__(self, q=1e-4, r=1e-1):
        self.q = q # Process noise
        self.r = r # Measurement noise
        self.x = None
        self.p = 1.0

    def update(self, z):
        if self.x is None:
            self.x = z
            return self.x
        
        # Predict
        p_prio = self.p + self.q
        
        # Update
        k = p_prio / (p_prio + self.r)
        self.x = self.x + k * (z - self.x)
        self.p = (1 - k) * p_prio
        return self.x

def apply_kalman_filter(df, columns):
    """
    Apply Kalman smoothing to specific columns to reduce noise and sensor drift.
    """
    df_smoothed = df.copy()
    for col in columns:
        if col not in df_smoothed.columns: continue
        kf = AdaptiveKalman()
        df_smoothed[col] = df_smoothed[col].apply(lambda x: kf.update(x))
    
    print(f"[Step 2: Kalman] Smoothed {len(columns)} sensor streams for signal stability.")
    return df_smoothed

if __name__ == "__main__":
    df = pd.read_csv("data/raw_telemetry/sample_orbit_data.csv")
    df = apply_kalman_filter(df, ['battery_voltage', 'temp_celsius'])
