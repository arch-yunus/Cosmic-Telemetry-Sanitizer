import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_telemetry(n_rows=1000):
    start_time = datetime(2026, 3, 28, 22, 0, 0)
    timestamps = [start_time + timedelta(seconds=i) for i in range(n_rows)]
    
    # Base signals (clean)
    t = np.linspace(0, 10, n_rows)
    battery_voltage = 28.0 + 0.5 * np.sin(t) + np.random.normal(0, 0.05, n_rows)
    bus_current = 2.0 + 0.2 * np.cos(t) + np.random.normal(0, 0.02, n_rows)
    temp_celsius = 25.0 + 2.0 * np.sin(t/2) + np.random.normal(0, 0.1, n_rows)
    rw_speed_rpm = 1500 + 500 * np.sin(t/4) + np.random.normal(0, 5, n_rows)
    sun_sensor_lux = 10000 * np.maximum(0, np.sin(t/3)) + np.random.normal(0, 50, n_rows)
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'battery_voltage': battery_voltage,
        'bus_current': bus_current,
        'temp_celsius': temp_celsius,
        'rw_speed_rpm': rw_speed_rpm,
        'sun_sensor_lux': sun_sensor_lux,
        'subsystem_status': [1] * n_rows
    })
    
    # Inject Point Anomalies (Spikes/Bit-flips)
    indices = np.random.choice(range(n_rows), size=15, replace=False)
    for idx in indices:
        col = np.random.choice(['battery_voltage', 'temp_celsius', 'rw_speed_rpm'])
        if col == 'battery_voltage': df.loc[idx, col] = 400.0 # SEU simulation
        if col == 'temp_celsius': df.loc[idx, col] = -150.0 # Sensor glitch
        if col == 'rw_speed_rpm': df.loc[idx, col] = 99999.0 # Overflow simulation

    # Inject Contextual Anomalies (Physically impossible correlations)
    # High current but battery voltage is dropping too fast or status is 0
    df.loc[500:510, 'bus_current'] = 50.0 # Huge draw
    df.loc[500:510, 'subsystem_status'] = 0 # But status says OFF (Anomaly!)
    
    # Inject Sensor Drift
    df.loc[800:, 'temp_celsius'] += np.linspace(0, 20, n_rows - 800)

    # NEW: Inject Sensor Stalling (Flatline)
    df.loc[200:230, 'rw_speed_rpm'] = df.loc[200, 'rw_speed_rpm']

    # NEW: Inject Periodic Interference (Sine gürültüsü)
    interference = 5.0 * np.sin(np.linspace(0, 50, 100))
    df.loc[600:699, 'sun_sensor_lux'] += interference
    
    os.makedirs('data/raw_telemetry', exist_ok=True)
    df.to_csv('data/raw_telemetry/sample_orbit_data.csv', index=False)
    print(f"Generated {n_rows} rows of telemetry data in data/raw_telemetry/sample_orbit_data.csv")

if __name__ == "__main__":
    generate_telemetry()
