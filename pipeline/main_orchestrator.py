import os
import json
import pandas as pd
import argparse
import sys
import logging

# Existing steps
from step1_mad_filter import apply_mad_filter
from step2_kalman_smooth import apply_kalman_filter
from step3_autoencoder import check_contextual_anomalies

# New steps
from step4_spectral_denoise import apply_spectral_denoising
from step5_physical_bounds import apply_physical_bounds

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def load_config(config_path="config/settings.json"):
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load config from {config_path}: {e}")
        return {}

def run_sanitization_pipeline(input_path, output_path, config=None):
    if config is None:
        config = load_config()
        
    logging.info("="*60)
    logging.info(" COSMIC TELEMETRY SANITIZER - UNIVERSAL FIDELITY PIPELINE")
    logging.info("="*60)
    
    # Load data
    if not os.path.exists(input_path):
        logging.error(f"Input file {input_path} not found.")
        sys.exit(1)
        
    df = pd.read_csv(input_path)
    cols_to_clean = config.get("columns_to_process", [])
    
    # 1. Statistical Outlier Removal (MAD)
    df = apply_mad_filter(df, cols_to_clean, 
                          window=config["mad_filter"]["window"], 
                          threshold=config["mad_filter"]["threshold"])
    
    # 2. Dynamical Smoothing (Kalman)
    df = apply_kalman_filter(df, cols_to_clean) # Uses internal defaults, could be extended
    
    # 3. AI-Based Contextual Correction (Isolation Forest)
    df = check_contextual_anomalies(df, cols_to_clean)
    
    # 4. Spectral Denoising (Butterworth Low-pass)
    df = apply_spectral_denoising(df, cols_to_clean, 
                                 order=config["spectral_denoise"]["order"], 
                                 cutoff=config["spectral_denoise"]["cutoff"])
    
    # 5. Physical Bound Enforcement (Final Safety Layer)
    df = apply_physical_bounds(df, config["physical_bounds"])
    
    # Save results
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    logging.info("="*60)
    logging.info(f"Pipeline Execution Successful.")
    logging.info(f"Output: {output_path}")
    logging.info("="*60)
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cosmic Telemetry Sanitizer Orchestrator")
    parser.add_argument("--input", default="data/raw_telemetry/sample_orbit_data.csv", help="Path to raw telemetry CSV")
    parser.add_argument("--output", default="data/sanitized_telemetry/cleaned_orbit_data.csv", help="Path to save sanitized CSV")
    parser.add_argument("--config", default="config/settings.json", help="Path to config JSON")
    
    args = parser.parse_args()
    config_data = load_config(args.config)
    run_sanitization_pipeline(args.input, args.output, config_data)
