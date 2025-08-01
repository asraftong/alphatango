# utils/latency_tracker.py

latency_samples = []

def record_latency(sample_ms: float):
    """Simpan sampel latency dalam senarai (maks 100)."""
    latency_samples.append(sample_ms)
    if len(latency_samples) > 100:
        latency_samples.pop(0)

def get_average_latency():
    """Kira purata latency daripada sampel."""
    if not latency_samples:
        return 0.0
    return sum(latency_samples) / len(latency_samples)
