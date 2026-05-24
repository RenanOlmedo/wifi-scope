
from analytics.channel_analysis import analyze_channels
from analytics.bssid_analysis import analyze_bssid
from analytics.anomaly_analysis import detect_network_anomalies
from processing.cleaning import clean_data
from processing.feature_engineering import create_features
from analytics.network_analysis import analyze_networks
from reporting.report_generator import generate_report
from analytics.rf_health_score import (
    calculate_rf_health_score
)
from analytics.channel_recommendation import (
    recommend_best_channel
)

from visualization.plots import (
    generate_all_plots
)

from collector.google_sheets_collector import (
    collect_google_sheets_data
)

from analytics.rf_peak_hours import (
    analyze_rf_peak_hours
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
channel_recommendation, best_channel = recommend_best_channel(df)
bssid_summary = analyze_bssid(df)
anomalies_df = detect_network_anomalies(df)
rf_health = calculate_rf_health_score(
    df,
    anomalies_df
)

rf_peak_hours, peak_hour = analyze_rf_peak_hours(df)
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