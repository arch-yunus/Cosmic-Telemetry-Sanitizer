import numpy as np
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def apply_mad_filter(df, columns, window=15, threshold=3.5):
    """
    Apply a Median Absolute Deviation (MAD) filter to remove point anomalies.

    Parameters
    ----------
    df : pandas.DataFrame
        Input telemetry dataframe.
    columns : list[str]
        List of column names to filter.
    window : int, optional
        Rolling window size for median and MAD calculation. Default is 15.
    threshold : float, optional
        Z‑score threshold for outlier detection. Default is 3.5.

    Returns
    -------
    pandas.DataFrame
        A copy of ``df`` with outliers replaced by the rolling median.
    """
    df_clean = df.copy()
    anomalies_count = 0

    for col in columns:
        if col not in df_clean.columns:
            continue
        # Rolling median and MAD
        rolling_median = df_clean[col].rolling(window=window, center=True).median()
        rolling_median = rolling_median.ffill().bfill()
        abs_deviation = (df_clean[col] - rolling_median).abs()
        mad = abs_deviation.rolling(window=window, center=True).median()
        mad = mad.ffill().bfill()
        mad = mad.replace(0, 1e-6)  # avoid division by zero
        # Modified Z‑score
        z_score = 0.6745 * (df_clean[col] - rolling_median) / mad
        outliers = z_score.abs() > threshold
        anomalies_count += outliers.sum()
        # Impute outliers with rolling median
        df_clean.loc[outliers, col] = rolling_median[outliers]

    logging.info(f"[Step 1: MAD] Scanned {len(columns)} columns. Found and mitigated {anomalies_count} point anomalies.")
    return df_clean

if __name__ == "__main__":
    df = pd.read_csv("data/raw_telemetry/sample_orbit_data.csv")
    cols = ["battery_voltage", "temp_celsius", "rw_speed_rpm"]
    df_filtered = apply_mad_filter(df, cols)
