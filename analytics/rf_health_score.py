import pandas as pd
from pathlib import Path


def calculate_rf_health_score(
    df,
    anomalies_df
):

    print("Calculando RF Health Score...")

    avg_rssi = df["rssi"].mean()

    total_networks = df["ssid"].nunique()

    total_anomalies = len(anomalies_df)

    rssi_std = df["rssi"].std()

    total_records = len(df)

    # =========================
    # SCORE RSSI
    # =========================

    rssi_score = max(
        0,
        min(
            100,
            avg_rssi + 100
        )
    )

    # =========================
    # SCORE CONGESTIONAMENTO
    # =========================

    congestion_score = max(
        0,
        100 - (total_networks * 5)
    )

    # =========================
    # SCORE ESTABILIDADE
    # =========================

    stability_score = max(
        0,
        100 - (rssi_std * 5)
    )

    # =========================
    # SCORE ANOMALIAS
    # =========================

    anomaly_ratio = (
        total_anomalies / total_records
        if total_records > 0
        else 0
    )

    anomaly_score = max(
        0,
        100 - (anomaly_ratio * 100)
    )

    # =========================
    # SCORE FINAL
    # =========================

    final_score = (
        rssi_score * 0.35
        + congestion_score * 0.25
        + stability_score * 0.25
        + anomaly_score * 0.15
    )

    final_score = round(final_score, 2)

    # =========================
    # CLASSIFICACAO
    # =========================

    if final_score >= 85:
        status = "Excelente"

    elif final_score >= 70:
        status = "Bom"

    elif final_score >= 50:
        status = "Moderado"

    else:
        status = "Ruim"

    result = pd.DataFrame([{
        "rf_health_score": final_score,
        "status": status,
        "avg_rssi": round(avg_rssi, 2),
        "total_networks": total_networks,
        "total_anomalies": total_anomalies,
        "anomaly_ratio_percent": round(
            anomaly_ratio * 100,
            2
        ),
        "rssi_std": round(rssi_std, 2)
    }])

    output_path = Path(
        "data/processed/rf_health_score.csv"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    result.to_csv(
        output_path,
        index=False
    )

    print("RF Health Score salvo em:")
    print(output_path)

    print(f"RF Health Score: {final_score}")

    print(f"Status RF: {status}")

    return result