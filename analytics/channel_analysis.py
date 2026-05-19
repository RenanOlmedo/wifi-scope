from pathlib import Path


def analyze_channels(df):

    print("Analisando canais Wi-Fi...")

    channel_summary = (
        df.groupby("channel")
        .agg(
            detections=("channel", "count"),
            avg_rssi=("rssi", "mean"),
            best_rssi=("rssi", "max"),
            worst_rssi=("rssi", "min"),
            unique_networks=("ssid", "nunique"),
            unique_aps=("bssid", "nunique")
        )
        .reset_index()
    )

    channel_summary["avg_rssi"] = (
        channel_summary["avg_rssi"]
        .round(2)
    )

    channel_summary["channel_load_score"] = (
        channel_summary["detections"]
        * channel_summary["unique_aps"]
    )

    output_path = Path(
        "data/processed/channel_summary.csv"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    channel_summary.to_csv(
        output_path,
        index=False
    )

    most_used_channel = (
        channel_summary
        .sort_values(
            "detections",
            ascending=False
        )
        .iloc[0]
    )

    print("Resumo de canais salvo em:")
    print(output_path)

    print(
        f"Canal mais usado: {int(most_used_channel['channel'])}"
    )

    return channel_summary