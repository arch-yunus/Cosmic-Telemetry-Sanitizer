import numpy as np
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def apply_physical_bounds(df, bounds):
    """
    Step 5: Verifies that telemetry data stays within physically possible ranges.
    Clips extreme values that might have survived previous filter layers.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Telemetry data.
    bounds : dict
        A dictionary mapping column names to [min, max] list.
    """
    df_clean = df.copy()
    clamped_count = 0
    
    for col, (min_val, max_val) in bounds.items():
        if col not in df_clean.columns:
            continue
            
        out_of_bounds = (df_clean[col] < min_val) | (df_clean[col] > max_val)
        clamped_count += out_of_bounds.sum()
        
        # Clip the values to the bounds
        df_clean[col] = df_clean[col].clip(lower=min_val, upper=max_val)
        
    logging.info(f"[Step 5: Safety] Enforced Physical Bounds. Clamped {clamped_count} outliers across {len(bounds)} sensors.")
    return df_clean

if __name__ == "__main__":
    df = pd.DataFrame({'battery_voltage': [28.0, 400.0, -10.0]})
    bounds = {'battery_voltage': [10.0, 36.0]}
    df_clamped = apply_physical_bounds(df, bounds)
    print(df_clamped)
