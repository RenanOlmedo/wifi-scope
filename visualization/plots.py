import matplotlib.pyplot as plt
from pathlib import Path


REPORTS_PATH = Path("data/reports")


def ensure_reports_folder():

    REPORTS_PATH.mkdir(
        parents=True,
        exist_ok=True
    )


def plot_top_networks(network_summary):

    print("Gerando gráfico: top redes...")

    ensure_reports_folder()

    top_networks = (
        network_summary
        .sort_values("detections", ascending=False)
        .head(10)
    )

    plt.figure(figsize=(12, 6))
    plt.bar(top_networks["ssid"], top_networks["detections"])

    plt.title("Top Redes Mais Detectadas")
    plt.xlabel("SSID")
    plt.ylabel("Detecções")
    plt.xticks(rotation=20)
    plt.tight_layout()

    output_path = REPORTS_PATH / "top_networks.png"

    plt.savefig(output_path)
    plt.close()

    print("Gráfico salvo:")
    print(output_path)


def plot_strongest_networks(network_summary):

    print("Gerando gráfico: redes mais fortes...")

    ensure_reports_folder()

    strongest = (
        network_summary
        .sort_values("avg_rssi", ascending=False)
        .head(10)
    )

    plt.figure(figsize=(12, 6))
    plt.bar(strongest["ssid"], strongest["avg_rssi"])

    plt.title("Top Redes com Melhor Sinal Médio")
    plt.xlabel("SSID")
    plt.ylabel("RSSI médio (dBm)")
    plt.xticks(rotation=20)
    plt.tight_layout()

    output_path = REPORTS_PATH / "strongest_networks.png"

    plt.savefig(output_path)
    plt.close()

    print("Gráfico salvo:")
    print(output_path)


def plot_most_unstable_networks(network_summary):

    print("Gerando gráfico: redes mais instáveis...")

    ensure_reports_folder()

    unstable = (
        network_summary
        .sort_values("rssi_std", ascending=False)
        .head(10)
    )

    plt.figure(figsize=(12, 6))
    plt.bar(unstable["ssid"], unstable["rssi_std"])

    plt.title("Top Redes Mais Instáveis")
    plt.xlabel("SSID")
    plt.ylabel("Desvio padrão do RSSI")
    plt.xticks(rotation=20)
    plt.tight_layout()

    output_path = REPORTS_PATH / "most_unstable_networks.png"

    plt.savefig(output_path)
    plt.close()

    print("Gráfico salvo:")
    print(output_path)


def plot_channel_distribution(df):

    print("Gerando gráfico: distribuição de canais...")

    ensure_reports_folder()

    channel_counts = (
        df["channel"]
        .value_counts()
        .sort_index()
    )

    plt.figure(figsize=(10, 6))
    plt.bar(channel_counts.index, channel_counts.values)

    plt.title("Distribuição de Redes por Canal")
    plt.xlabel("Canal Wi-Fi")
    plt.ylabel("Quantidade de detecções")
    plt.tight_layout()

    output_path = REPORTS_PATH / "channel_distribution.png"

    plt.savefig(output_path)
    plt.close()

    print("Gráfico salvo:")
    print(output_path)


def plot_rssi_timeline(df):

    print("Gerando gráfico: RSSI ao longo do tempo...")

    ensure_reports_folder()

    top_ssids = (
        df["ssid"]
        .value_counts()
        .head(5)
        .index
    )

    filtered = df[
        df["ssid"].isin(top_ssids)
    ]

    plt.figure(figsize=(14, 7))

    for ssid in top_ssids:

        ssid_df = filtered[
            filtered["ssid"] == ssid
        ]

        plt.plot(
            ssid_df["timestamp"],
            ssid_df["rssi"],
            marker="o",
            label=ssid
        )

    plt.title("RSSI ao Longo do Tempo - Top Redes")
    plt.xlabel("Tempo")
    plt.ylabel("RSSI (dBm)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    output_path = REPORTS_PATH / "rssi_timeline.png"

    plt.savefig(output_path)
    plt.close()

    print("Gráfico salvo:")
    print(output_path)


def plot_channel_load_score(channel_summary):

    print("Gerando gráfico: carga dos canais...")

    ensure_reports_folder()

    channel_summary = (
        channel_summary
        .sort_values("channel")
    )

    plt.figure(figsize=(10, 6))

    plt.bar(
        channel_summary["channel"],
        channel_summary["channel_load_score"]
    )

    plt.title("Score de Carga por Canal")
    plt.xlabel("Canal Wi-Fi")
    plt.ylabel("Channel Load Score")
    plt.tight_layout()

    output_path = REPORTS_PATH / "channel_load_score.png"

    plt.savefig(output_path)
    plt.close()

    print("Gráfico salvo:")
    print(output_path)


def plot_avg_rssi_by_channel(channel_summary):

    print("Gerando gráfico: RSSI médio por canal...")

    ensure_reports_folder()

    channel_summary = (
        channel_summary
        .sort_values("channel")
    )

    plt.figure(figsize=(10, 6))

    plt.bar(
        channel_summary["channel"],
        channel_summary["avg_rssi"]
    )

    plt.title("RSSI Médio por Canal")
    plt.xlabel("Canal Wi-Fi")
    plt.ylabel("RSSI médio (dBm)")
    plt.tight_layout()

    output_path = REPORTS_PATH / "avg_rssi_by_channel.png"

    plt.savefig(output_path)
    plt.close()

    print("Gráfico salvo:")
    print(output_path)


def plot_bssid_presence(bssid_summary):

    print("Gerando gráfico: presença por BSSID...")

    ensure_reports_folder()

    top_bssid = (
        bssid_summary
        .sort_values("presence_score", ascending=False)
        .head(10)
    )

    labels = (
        top_bssid["ssid"].astype(str)
        + "\n"
        + top_bssid["bssid"].astype(str)
    )

    plt.figure(figsize=(14, 7))

    plt.bar(
        labels,
        top_bssid["presence_score"]
    )

    plt.title("Top BSSID/APs por Presença")
    plt.xlabel("SSID / BSSID")
    plt.ylabel("Presence Score (%)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    output_path = REPORTS_PATH / "bssid_presence.png"

    plt.savefig(output_path)
    plt.close()

    print("Gráfico salvo:")
    print(output_path)


def plot_bssid_stability(bssid_summary):

    print("Gerando gráfico: estabilidade por BSSID...")

    ensure_reports_folder()

    stable = (
        bssid_summary
        .sort_values("stability_score", ascending=False)
        .head(10)
    )

    labels = (
        stable["ssid"].astype(str)
        + "\n"
        + stable["bssid"].astype(str)
    )

    plt.figure(figsize=(14, 7))

    plt.bar(
        labels,
        stable["stability_score"]
    )

    plt.title("Top BSSID/APs Mais Estáveis")
    plt.xlabel("SSID / BSSID")
    plt.ylabel("Stability Score (%)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    output_path = REPORTS_PATH / "bssid_stability.png"

    plt.savefig(output_path)
    plt.close()

    print("Gráfico salvo:")
    print(output_path)


def plot_anomaly_types(anomalies_df):

    print("Gerando gráfico: tipos de anomalias...")

    ensure_reports_folder()

    if anomalies_df.empty:
        print("Nenhuma anomalia para plotar.")
        return

    anomaly_counts = (
        anomalies_df["anomaly_type"]
        .value_counts()
    )

    plt.figure(figsize=(12, 6))

    plt.bar(
        anomaly_counts.index,
        anomaly_counts.values
    )

    plt.title("Distribuição dos Tipos de Anomalia")
    plt.xlabel("Tipo de anomalia")
    plt.ylabel("Quantidade")
    plt.xticks(rotation=20)
    plt.tight_layout()

    output_path = REPORTS_PATH / "anomaly_types.png"

    plt.savefig(output_path)
    plt.close()

    print("Gráfico salvo:")
    print(output_path)


def plot_quality_distribution(df):

    print("Gerando gráfico: distribuição de qualidade...")

    ensure_reports_folder()

    quality_counts = (
        df["signal_classification"]
        .value_counts()
    )

    plt.figure(figsize=(10, 6))

    plt.bar(
        quality_counts.index,
        quality_counts.values
    )

    plt.title("Distribuição da Qualidade de Sinal")
    plt.xlabel("Classificação")
    plt.ylabel("Quantidade de detecções")
    plt.tight_layout()

    output_path = REPORTS_PATH / "quality_distribution.png"

    plt.savefig(output_path)
    plt.close()

    print("Gráfico salvo:")
    print(output_path)

def plot_rf_peak_hours(rf_peak_hours):

    print("Gerando gráfico: pico RF por horário...")

    ensure_reports_folder()

    hourly = (
        rf_peak_hours
        .sort_values("hour")
    )

    plt.figure(figsize=(12, 6))

    plt.bar(
        hourly["hour"],
        hourly["rf_load_score"]
    )

    plt.title("Carga RF por Horário do Dia")
    plt.xlabel("Hora do dia")
    plt.ylabel("RF Load Score")

    plt.xticks(
        range(0, 24)
    )

    plt.tight_layout()

    output_path = REPORTS_PATH / "rf_peak_hours.png"

    plt.savefig(output_path)
    plt.close()

    print("Gráfico salvo:")
    print(output_path)


def generate_all_plots(
    df,
    network_summary,
    channel_summary,
    bssid_summary,
    anomalies_df,
    rf_peak_hours
):

    plot_top_networks(network_summary)
    plot_strongest_networks(network_summary)
    plot_most_unstable_networks(network_summary)
    plot_channel_distribution(df)
    plot_rssi_timeline(df)

    plot_channel_load_score(channel_summary)
    plot_avg_rssi_by_channel(channel_summary)
    plot_bssid_presence(bssid_summary)
    plot_bssid_stability(bssid_summary)
    plot_anomaly_types(anomalies_df)
    plot_quality_distribution(df)
    plot_rf_peak_hours(rf_peak_hours)