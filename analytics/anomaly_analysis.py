from pathlib import Path


def detect_network_anomalies(df):

    print("Detectando anomalias wireless...")

    anomalies = []

    # Redes com sinal muito fraco
    weak_signal = df[
        df["rssi"] <= -85
    ].copy()

    weak_signal["anomaly_type"] = "Sinal muito fraco"

    anomalies.append(weak_signal)

    # Redes com sinal extremamente forte
    very_strong_signal = df[
        df["rssi"] >= -35
    ].copy()

    very_strong_signal["anomaly_type"] = "Sinal extremamente forte"

    anomalies.append(very_strong_signal)

    # Redes novas detectadas apenas uma vez
    counts = (
        df.groupby("bssid")
        .size()
        .reset_index(name="count")
    )

    rare_bssids = counts[
        counts["count"] == 1
    ]["bssid"]

    rare_networks = df[
        df["bssid"].isin(rare_bssids)
    ].copy()

    rare_networks["anomaly_type"] = "Rede detectada apenas uma vez"

    anomalies.append(rare_networks)

    if anomalies:

        anomalies_df = (
            __import__("pandas")
            .concat(
                anomalies,
                ignore_index=True
            )
        )

    else:

        anomalies_df = df.iloc[0:0].copy()

    output_path = Path(
        "data/processed/wireless_anomalies.csv"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    anomalies_df.to_csv(
        output_path,
        index=False
    )

    print("Anomalias salvas em:")
    print(output_path)

    print(
        f"Total de anomalias detectadas: {len(anomalies_df)}"
    )

    return anomalies_df