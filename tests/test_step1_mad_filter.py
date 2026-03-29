import pandas as pd
import numpy as np
from pipeline.step1_mad_filter import apply_mad_filter

def test_mad_filter_removes_spikes():
    # Create synthetic data with a spike
    data = {
        "battery_voltage": [30, 30, 1000, 30, 30],
        "temp_celsius": [20, 20, 20, 20, 20],
    }
    df = pd.DataFrame(data)
    cleaned = apply_mad_filter(df, ["battery_voltage", "temp_celsius"], window=3, threshold=3.5)
    # Spike should be replaced by median (30)
    assert cleaned.loc[2, "battery_voltage"] == 30
    # No changes to other column
    assert cleaned["temp_celsius"].tolist() == [20, 20, 20, 20, 20]
