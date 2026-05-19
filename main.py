
from analytics.channel_analysis import analyze_channels
from analytics.bssid_analysis import analyze_bssid
from analytics.anomaly_analysis import detect_network_anomalies
from processing.cleaning import clean_data
from processing.feature_engineering import create_features
from analytics.network_analysis import analyze_networks
from reporting.report_generator import generate_report

from visualization.plots import (
    generate_all_plots
)

from collector.google_sheets_collector import (
    collect_google_sheets_data
)

print()
print("===================================")
print("INICIANDO WIFI SCOPE")
print("===================================")

df = collect_google_sheets_data()


print()
print("Coleta concluída com sucesso!")

print()
print(df.head())
df = clean_data(df)
df = create_features(df)
network_summary = analyze_networks(df)
channel_summary = analyze_channels(df)
bssid_summary = analyze_bssid(df)
anomalies_df = detect_network_anomalies(df)
generate_all_plots(
    df,
    network_summary,
    channel_summary,
    bssid_summary,
    anomalies_df
)

# generate_report(
#     df,
#     network_summary,
#     channel_summary,
#     bssid_summary,
#     anomalies_df
# )