import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_comparison_plots(raw_path, sanitized_path):
    raw_df = pd.read_csv(raw_path)
    clean_df = pd.read_csv(sanitized_path)
    
    # Use a subset for clear visualization
    subset_range = (400, 700) # Region with injected anomalies
    
    raw_sub = raw_df.iloc[subset_range[0]:subset_range[1]]
    clean_sub = clean_df.iloc[subset_range[0]:subset_range[1]]
    
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    
    # Battery Voltage Plot
    axes[0].plot(raw_sub['battery_voltage'], label='Raw (Anomalous)', color='red', alpha=0.5)
    axes[0].plot(clean_sub['battery_voltage'], label='Sanitized', color='green', linewidth=1.5)
    axes[0].set_title('Battery Voltage Sanitization (SEU Mitigation)')
    axes[0].legend()
    
    # Temperature Plot
    axes[1].plot(raw_sub['temp_celsius'], label='Raw (Drift/Spikes)', color='orange', alpha=0.5)
    axes[1].plot(clean_sub['temp_celsius'], label='Sanitized', color='blue', linewidth=1.5)
    axes[1].set_title('Thermal Data Smoothing & Correction')
    axes[1].legend()
    
    # Bus Current Plot
    axes[2].plot(raw_sub['bus_current'], label='Raw (Contextual Anomaly)', color='purple', alpha=0.5)
    axes[2].plot(clean_sub['bus_current'], label='Sanitized', color='black', linewidth=1.5)
    axes[2].set_title('Bus Current Correlation Correction')
    axes[2].legend()
    
    plt.tight_layout()
    os.makedirs('notebooks', exist_ok=True)
    plot_path = 'notebooks/sanitization_results.png'
    plt.savefig(plot_path)
    print(f"Visualization saved to: {plot_path}")

if __name__ == "__main__":
    generate_comparison_plots('data/raw_telemetry/sample_orbit_data.csv', 'data/sanitized_telemetry/cleaned_orbit_data.csv')
