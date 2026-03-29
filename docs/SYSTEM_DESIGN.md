# 🛰️ Cosmic-Telemetry-Sanitizer: System Design & Mathematical Foundation

## 1. Overview
The **Cosmic-Telemetry-Sanitizer** is a multi-stage filtering pipeline designed to protect satellite ground-segment software from Single Event Upsets (SEUs) and sensor-level anomalies caused by space radiation.

## 2. Pipeline Stages

### Stage 1: Median Absolute Deviation (MAD)
Initial spike removal using a rolling window. For a measurement $x_i$, the modified Z-score is:
$$M_i = \frac{0.6745(x_i - \tilde{x})}{\text{MAD}}$$
where $\tilde{x}$ is the median and $\text{MAD} = \text{median}(|x_i - \tilde{x}|)$. If $|M_i| > \text{threshold}$, $x_i$ is treated as a bit-flip and replaced.

### Stage 2: Adaptive Kalman Filtering
Scalar state estimation to dampen Gaussian noise.
- **Predict**: $\hat{x}_k^- = \hat{x}_{k-1}$
- **Update**: $K_k = P_k^- (P_k^- + R)^{-1}$, $\hat{x}_k = \hat{x}_k^- + K_k(z_k - \hat{x}_k^-)$

### Stage 3: Multivariate Isolation Forest
Detects contextual anomalies where individual sensors are within limits but their *relationship* is physically impossible.
- Trains an ensemble of isolation trees.
- Anomalies are those with short average path lengths in the trees.

### Stage 4: Butterworth Low-Pass Filter
Removes high-frequency jitter. The transfer function in the s-domain is:
$$|H(j\omega)| = \frac{1}{\sqrt{1 + (\frac{\omega}{\omega_c})^{2n}}}$$
We use `filtfilt` for zero-phase distortion, ensuring real-time telemetry events align with their timestamps.

### Stage 5: Rule-Based Physical Bounds
The final guardrail. Any value exceeding pre-defined satellite bus limits (e.g., Battery > 36V) is clipped to the nearest safe boundary.

## 3. Configuration Management
All parameters are stored in `config/settings.json`, allowing mission controllers to tune sensitivity without re-compiling the pipeline.
