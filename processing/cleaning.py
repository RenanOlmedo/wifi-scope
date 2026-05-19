import pandas as pd
from pathlib import Path

from config import PROCESSED_DATA_PATH


def clean_data(df):

    print("Limpando dados...")

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        dayfirst=True,
        errors="coerce"
    )

    df["ssid"] = df["ssid"].astype(str).str.strip()
    df["bssid"] = df["bssid"].astype(str).str.strip()
    df["encryption"] = df["encryption"].astype(str).str.strip()

    df["rssi"] = pd.to_numeric(
        df["rssi"],
        errors="coerce"
    )

    df["channel"] = pd.to_numeric(
        df["channel"],
        errors="coerce"
    )

    df.dropna(inplace=True)

    df.sort_values(
        "timestamp",
        inplace=True
    )

    output_path = Path(PROCESSED_DATA_PATH)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_path,
        index=False
    )

    print(f"Dados processados salvos em: {PROCESSED_DATA_PATH}")
    print(f"Registros válidos: {len(df)}")

    return df