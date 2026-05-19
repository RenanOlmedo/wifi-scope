from pathlib import Path


def analyze_networks(df):

    print("Analisando redes individuais...")

    network_summary = (
        df.groupby(["ssid", "bssid"])
        .agg(
            detections=("ssid", "count"),
            avg_rssi=("rssi", "mean"),
            best_rssi=("rssi", "max"),
            worst_rssi=("rssi", "min"),
            rssi_std=("rssi", "std"),
            avg_quality=("signal_quality_score", "mean"),
            most_common_channel=("channel", lambda x: x.mode()[0]),
            encryption=("encryption", lambda x: x.mode()[0])
        )
        .reset_index()
    )

    network_summary["avg_rssi"] = network_summary["avg_rssi"].round(2)
    network_summary["rssi_std"] = network_summary["rssi_std"].fillna(0).round(2)
    network_summary["avg_quality"] = network_summary["avg_quality"].round(2)

    output_path = Path(
        "data/processed/network_summary.csv"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    network_summary.to_csv(
        output_path,
        index=False
    )

    print("Resumo por rede salvo em:")
    print(output_path)

    return network_summary