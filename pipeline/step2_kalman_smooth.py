import numpy as np
import pandas as pd

class SimpleKalmanFilter:
    def __init__(self, q=1e-5, r=1e-2):
        self.q = q # Process noise covariance
        self.r = r # Measurement noise covariance
        self.x = None # Initial state
        self.p = 1.0 # Initial error covariance

    def update(self, measurement):
        if self.x is None:
            self.x = measurement
            return self.x

        # Prediction
        p_prior = self.p + self.q
        
        # Update
        k = p_prior / (p_prior + self.r)
        self.x = self.x + k * (measurement - self.x)
        self.p = (1 - k) * p_prior
        
        return self.x

def apply_kalman_filter(df, column):
    kf = SimpleKalmanFilter()
    df[column] = df[column].apply(lambda x: kf.update(x))
    print(f"[Kalman Filter] Smoothed {column} using dynamic state estimation.")
    return df

if __name__ == "__main__":
    # Test logic
    data = {'val': [10, 11, 12, 11, 13]}
    df = pd.DataFrame(data)
    df_filtered = apply_kalman_filter(df, 'val')
    print(df_filtered)
