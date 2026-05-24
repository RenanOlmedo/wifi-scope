from pathlib import Path


def recommend_best_channel(df):

    print("Calculando recomendação automática de canal...")

    all_channels = list(range(1, 14))

    channel_data = []

    for channel in all_channels:

        channel_df = df[
            df["channel"] == channel
        ]

        detections = len(channel_df)

        unique_aps = (
            channel_df["bssid"].nunique()
            if not channel_df.empty
            else 0
        )

        avg_rssi = (
            channel_df["rssi"].mean()
            if not channel_df.empty
            else -100
        )

        # Quanto menor, melhor.
        # Penaliza canais com muitas redes e sinais fortes próximos.
        interference_score = (
            detections * 2
            + unique_aps * 5
            + max(0, avg_rssi + 100)
        )

        # Canais clássicos não sobrepostos no 2.4 GHz
        if channel in [1, 6, 11]:
            interference_score -= 10

        channel_data.append({
            "channel": channel,
            "detections": detections,
            "unique_aps": unique_aps,
            "avg_rssi": round(avg_rssi, 2),
            "interference_score": round(interference_score, 2)
        })

    import pandas as pd

    recommendation_df = pd.DataFrame(channel_data)

    recommendation_df = (
        recommendation_df
        .sort_values(
            "interference_score",
            ascending=True
        )
    )

    best_channel = int(
        recommendation_df.iloc[0]["channel"]
    )

    output_path = Path(
        "data/processed/channel_recommendation.csv"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    recommendation_df.to_csv(
        output_path,
        index=False
    )

    print("Recomendação de canal salva em:")
    print(output_path)

    print(f"Canal recomendado: {best_channel}")

    return recommendation_df, best_channel