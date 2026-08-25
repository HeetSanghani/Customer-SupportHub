# 04 — REST Load Scaling Results

| Concurrency Level | Total Requests | Avg Latency | P50 | P95 | P99 | Error Rate |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1 User** | 100 | 39.51 ms | 38.34 ms | 44.02 ms | 61.14 ms | 0.0% |
| **5 Users** | 100 | 77.71 ms | 76.16 ms | 94.80 ms | 110.12 ms | 0.0% |
| **10 Users** | 100 | 133.90 ms | 135.83 ms | 166.59 ms | 208.29 ms | 0.0% |
| **25 Users** | 100 | 341.77 ms | 348.48 ms | 392.15 ms | 428.66 ms | 0.0% |
| **50 Users** | 200 | 677.56 ms | 682.06 ms | 805.98 ms | 869.30 ms | 0.0% |
| **100 Users** | 200 | 1137.26 ms | 1157.18 ms | 1504.26 ms | 1628.52 ms | 0.0% |
