from pathlib import Path


def analyze_bssid(df):

    print("Analisando BSSID/APs individuais...")

    bssid_summary = (
        df.groupby(["bssid", "ssid"])
        .agg(
            detections=("bssid", "count"),
            avg_rssi=("rssi", "mean"),
            best_rssi=("rssi", "max"),
            worst_rssi=("rssi", "min"),
            rssi_std=("rssi", "std"),
            channel=("channel", lambda x: x.mode()[0]),
            encryption=("encryption", lambda x: x.mode()[0]),
            first_seen=("timestamp", "min"),
            last_seen=("timestamp", "max")
        )
        .reset_index()
    )

    bssid_summary["avg_rssi"] = (
        bssid_summary["avg_rssi"]
        .round(2)
    )

    bssid_summary["rssi_std"] = (
        bssid_summary["rssi_std"]
        .fillna(0)
        .round(2)
    )

    bssid_summary["presence_score"] = (
        bssid_summary["detections"]
        / bssid_summary["detections"].max()
        * 100
    ).round(2)

    bssid_summary["stability_score"] = (
        100 - bssid_summary["rssi_std"] * 5
    ).clip(
        lower=0,
        upper=100
    ).round(2)

    output_path = Path(
        "data/processed/bssid_summary.csv"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    bssid_summary.to_csv(
        output_path,
        index=False
    )

    print("Resumo BSSID salvo em:")
    print(output_path)

    return bssid_summary