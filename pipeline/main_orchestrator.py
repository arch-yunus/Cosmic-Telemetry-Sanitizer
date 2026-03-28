import os
import pandas as pd
import argparse
import sys
from step1_mad_filter import apply_mad_filter
from step2_kalman_smooth import apply_kalman_filter
from step3_autoencoder import check_contextual_anomalies

def main(input_path, output_path):
    print("="*60)
    print(" COSMIC TELEMETRY SANITIZER - HIGH FIDELITY PIPELINE")
    print("="*60)
    
    # Load data
    if not os.path.exists(input_path):
        print(f"ERROR: Input file {input_path} not found.")
        sys.exit(1)
        
    df = pd.read_csv(input_path)
    cols_to_clean = ['battery_voltage', 'bus_current', 'temp_celsius', 'rw_speed_rpm', 'sun_sensor_lux']
    
    # 1. Statistical Outlier Removal
    df = apply_mad_filter(df, cols_to_clean)
    
    # 2. Dynamical Smoothing (Kalman)
    df = apply_kalman_filter(df, cols_to_clean)
    
    # 3. AI-Based Contextual Correction
    df = check_contextual_anomalies(df, cols_to_clean)
    
    # Save results
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print("="*60)
    print(f"Pipeline Execution Successful.")
    print(f"Output: {output_path}")
    print("="*60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cosmic Telemetry Sanitizer Orchestrator")
    parser.add_argument("--input", default="data/raw_telemetry/sample_orbit_data.csv", help="Path to raw telemetry CSV")
    parser.add_argument("--output", default="data/sanitized_telemetry/cleaned_orbit_data.csv", help="Path to save sanitized CSV")
    
    args = parser.parse_args()
    main(args.input, args.output)
