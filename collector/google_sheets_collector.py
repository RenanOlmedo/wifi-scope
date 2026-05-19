import pandas as pd
from pathlib import Path

from config import SHEET_CSV_URL, RAW_DATA_PATH


def collect_google_sheets_data():

    print("Baixando dados do Google Sheets...")

    df = pd.read_csv(SHEET_CSV_URL)

    output_path = Path(RAW_DATA_PATH)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_path,
        index=False
    )

    print(f"Dados brutos salvos em: {RAW_DATA_PATH}")
    print(f"Registros coletados: {len(df)}")

    return df