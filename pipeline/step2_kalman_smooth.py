import numpy as np
import pandas as pd
import logging
from typing import List

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


class AdaptiveKalman:
    """Simple adaptive Kalman filter for 1‑D scalar measurements.

    Parameters
    ----------
    q : float, optional
        Process noise covariance. Default is 1e-4.
    r : float, optional
        Measurement noise covariance. Default is 1e-1.
    """

    def __init__(self, q: float = 1e-4, r: float = 1e-1):
        self.q = q  # Process noise
        self.r = r  # Measurement noise
        self.x: float | None = None  # State estimate
        self.p: float = 1.0  # Estimate covariance

    def update(self, z: float) -> float:
        """Update the filter with a new measurement ``z``.

        Returns the updated state estimate.
        """
        if self.x is None:
            self.x = z
            logging.debug("Kalman init with measurement %s", z)
            return self.x
        # Predict step
        p_prio = self.p + self.q
        # Update step
        k = p_prio / (p_prio + self.r)
        self.x = self.x + k * (z - self.x)
        self.p = (1 - k) * p_prio
        logging.debug("Kalman update: z=%s, k=%s, x=%s", z, k, self.x)
        return self.x


def apply_kalman_filter(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Apply a Kalman smoother to selected columns.

    Parameters
    ----------
    df : pandas.DataFrame
        Input telemetry dataframe.
    columns : list[str]
        Column names to smooth.

    Returns
    -------
    pandas.DataFrame
        Dataframe with smoothed columns.
    """
    df_smoothed = df.copy()
    for col in columns:
        if col not in df_smoothed.columns:
            logging.warning("Column %s not found in dataframe; skipping.", col)
            continue
        kf = AdaptiveKalman()
        df_smoothed[col] = df_smoothed[col].apply(lambda x: kf.update(float(x)))
    logging.info("[Step 2: Kalman] Smoothed %d sensor streams for signal stability.", len(columns))
    return df_smoothed


if __name__ == "__main__":
    df = pd.read_csv("data/raw_telemetry/sample_orbit_data.csv")
    df = apply_kalman_filter(df, ["battery_voltage", "temp_celsius"])
    # Optionally save the smoothed data
    df.to_csv("data/processed/kalman_smoothed.csv", index=False)
