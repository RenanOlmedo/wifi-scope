import pandas as pd
from pathlib import Path


def analyze_rf_peak_hours(df):

    print("Analisando horários de pico RF...")

    df = df.copy()

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    df["hour"] = df["timestamp"].dt.hour

    hourly_summary = (
        df.groupby("hour")
        .agg({
            "ssid": "count",
            "rssi": "mean",
            "bssid": "nunique"
        })
        .reset_index()
    )

    hourly_summary.columns = [
        "hour",
        "detections",
        "avg_rssi",
        "unique_bssids"
    ]

    # =========================
    # SCORE DE CONGESTIONAMENTO
    # =========================

    hourly_summary["rf_load_score"] = (
        hourly_summary["detections"] * 0.6
        + hourly_summary["unique_bssids"] * 4
        + (100 + hourly_summary["avg_rssi"])
    )

    hourly_summary = hourly_summary.sort_values(
        "rf_load_score",
        ascending=False
    )

    peak_hour = int(
        hourly_summary.iloc[0]["hour"]
    )

    output_path = Path(
        "data/processed/rf_peak_hours.csv"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    hourly_summary.to_csv(
        output_path,
        index=False
    )

    print("Horários RF salvos em:")
    print(output_path)

    print(f"Horário de pico RF: {peak_hour}:00")

    return hourly_summary, peak_hour