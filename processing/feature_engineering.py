def rssi_to_quality_score(rssi):

    score = 2 * (rssi + 100)

    return max(
        0,
        min(100, score)
    )


def classify_signal(score):

    if score >= 85:
        return "Excelente"

    elif score >= 70:
        return "Bom"

    elif score >= 50:
        return "Moderado"

    elif score >= 30:
        return "Ruim"

    else:
        return "Crítico"


def create_features(df):

    print("Criando features...")

    df["signal_quality_score"] = (
        df["rssi"]
        .apply(rssi_to_quality_score)
    )

    df["signal_classification"] = (
        df["signal_quality_score"]
        .apply(classify_signal)
    )

    df["hour"] = (
        df["timestamp"]
        .dt.hour
    )

    df["date"] = (
        df["timestamp"]
        .dt.date
    )

    df["day_name"] = (
        df["timestamp"]
        .dt.day_name()
    )

    df["network_id"] = (
        df["ssid"].astype(str)
        + " | "
        + df["bssid"].astype(str)
    )

    print("Features criadas")

    return df