## Architecture Overview

```mermaid
flowchart TD
    A[Raw Telemetry CSV] --> B[Step 1: MAD Filter]
    B --> C[Step 2: Kalman Smoother]
    C --> D[Step 3: Autoencoder Anomaly Detection]
    D --> E[Sanitized Telemetry CSV]
    style A fill:#1f3b4d,color:#fff,stroke:#2e7d32,stroke-width:2px
    style B fill:#2e7d32,color:#fff,stroke:#1f3b4d,stroke-width:2px
    style C fill:#2e7d32,color:#fff,stroke:#1f3b4d,stroke-width:2px
    style D fill:#2e7d32,color:#fff,stroke:#1f3b4d,stroke-width:2px
    style E fill:#1f3b4d,color:#fff,stroke:#2e7d32,stroke-width:2px
```

The diagram illustrates the sequential processing pipeline:
1. **MAD Filter** removes point spikes.
2. **Kalman Smoother** reduces noise and imputes missing values.
3. **Autoencoder** detects contextual anomalies.
4. Output is a clean telemetry CSV ready for downstream analysis.
