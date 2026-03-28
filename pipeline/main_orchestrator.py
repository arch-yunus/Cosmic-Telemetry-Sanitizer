import os
import pandas as pd
import argparse
from step1_mad_filter import apply_mad_filter
from step2_kalman_smooth import apply_kalman_filter
from step3_autoencoder import check_contextual_anomalies

def main(input_path, output_path):
    print(f"--- Cosmic-Telemetry-Sanitizer Pipeline Starting ---")
    
    # Load data
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} not found.")
        return
        
    df = pd.read_csv(input_path)
    
    # Step 1: Statistical Filtering (Spike Removal)
    for col in ['battery_voltage', 'temp_celsius', 'rw_speed_rpm']:
        df = apply_mad_filter(df, col)
        
    # Step 2: Kalman Smoothing
    for col in ['battery_voltage', 'temp_celsius', 'rw_speed_rpm']:
        df = apply_kalman_filter(df, col)
        
    # Step 3: AI Contextual Check
    df = check_contextual_anomalies(df)
    
    # Save results
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"--- Sanitization Complete. Cleaned data saved to: {output_path} ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cosmic Telemetry Sanitizer Orchestrator")
    parser.add_argument("--input", default="data/raw_telemetry/sample_orbit_data.csv", help="Path to raw telemetry CSV")
    parser.add_argument("--output", default="data/sanitized_telemetry/cleaned_orbit_data.csv", help="Path to save sanitized CSV")
    
    args = parser.parse_args()
    main(args.input, args.output)
