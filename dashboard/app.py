import os
import subprocess
from pathlib import Path

import pandas as pd
import streamlit as st

from reporting.report_generator import generate_report
from processing.feature_engineering import create_features


# =========================
# CONFIGURAÇÃO
# =========================

st.set_page_config(
    page_title="WiFi Scope",
    page_icon="📡",
    layout="wide"
)

BASE_PATH = Path(".")
DATA_PATH = Path("data/processed/wifi_scope_processed.csv")
NETWORK_SUMMARY_PATH = Path("data/processed/network_summary.csv")
CHANNEL_SUMMARY_PATH = Path("data/processed/channel_summary.csv")
BSSID_SUMMARY_PATH = Path("data/processed/bssid_summary.csv")
ANOMALIES_PATH = Path("data/processed/wireless_anomalies.csv")
REPORTS_PATH = Path(
    "C:/Users/rferr/OneDrive/Documentos/wifi scope docs"
)


# =========================
# FUNÇÕES
# =========================

@st.cache_data
def load_data():

    df = pd.read_csv(DATA_PATH)
    network_summary = pd.read_csv(NETWORK_SUMMARY_PATH)
    channel_summary = pd.read_csv(CHANNEL_SUMMARY_PATH)
    bssid_summary = pd.read_csv(BSSID_SUMMARY_PATH)
    anomalies_df = pd.read_csv(ANOMALIES_PATH)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return (
        df,
        network_summary,
        channel_summary,
        bssid_summary,
        anomalies_df
    )


def run_full_pipeline():

    result = subprocess.run(
        ["python", "main.py"],
        capture_output=True,
        text=True
    )

    return result


def open_folder(path):

    folder_path = os.path.abspath(path)

    if os.path.exists(folder_path):
        os.startfile(folder_path)
    else:
        st.warning(f"Pasta não encontrada: {folder_path}")


def show_image(image_path, caption):

    if image_path.exists():
        st.image(str(image_path), caption=caption, use_container_width=True)


# =========================
# CABEÇALHO
# =========================

st.title("📡 WiFi Scope")
st.caption("Wireless Intelligence Platform | ESP8266 + Google Sheets + Python Analytics")

st.divider()


# =========================
# PAINEL DE CONTROLE
# =========================

st.subheader("🎛️ Central de Controle")

col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)

with col_btn1:

    if st.button("🔄 Atualizar Tudo", use_container_width=True):

        with st.spinner("Executando pipeline completo..."):

            result = run_full_pipeline()

            if result.returncode == 0:
                st.success("Pipeline executado com sucesso!")
                st.cache_data.clear()
                st.rerun()
            else:
                st.error("Erro ao executar pipeline.")
                st.text(result.stderr)

with col_btn2:

    if st.button("📄 Gerar Relatório DOCX", use_container_width=True):

        if (
            DATA_PATH.exists()
            and NETWORK_SUMMARY_PATH.exists()
            and CHANNEL_SUMMARY_PATH.exists()
            and BSSID_SUMMARY_PATH.exists()
            and ANOMALIES_PATH.exists()
        ):

            with st.spinner("Gerando relatório DOCX..."):

                df_report = pd.read_csv(DATA_PATH)
                network_summary_report = pd.read_csv(NETWORK_SUMMARY_PATH)
                channel_summary_report = pd.read_csv(CHANNEL_SUMMARY_PATH)
                bssid_summary_report = pd.read_csv(BSSID_SUMMARY_PATH)
                anomalies_report = pd.read_csv(ANOMALIES_PATH)

                df_report["timestamp"] = pd.to_datetime(
                    df_report["timestamp"]
                )
                df_report = create_features(df_report)

                output_path = generate_report(
                    df_report,
                    network_summary_report,
                    channel_summary_report,
                    bssid_summary_report,
                    anomalies_report
                )

                st.success("Relatório gerado com sucesso!")
                st.write(output_path)

        else:
            st.warning("Rode o pipeline pelo menos uma vez antes de gerar relatório.")

with col_btn3:

    if st.button("📂 Abrir Relatórios", use_container_width=True):

        open_folder(REPORTS_PATH)

with col_btn4:

    if st.button("🗂️ Abrir Projeto", use_container_width=True):

        open_folder(BASE_PATH)


col_btn5, col_btn6, col_btn7, col_btn8 = st.columns(4)

with col_btn5:

    if st.button("🧹 Limpar Cache", use_container_width=True):

        st.cache_data.clear()
        st.success("Cache limpo.")
        st.rerun()

with col_btn6:

    if st.button("📊 Abrir Dados Processados", use_container_width=True):

        open_folder("data/processed")

with col_btn7:

    if st.button("🖼️ Abrir Gráficos", use_container_width=True):

        open_folder("data/reports")

with col_btn8:

    if st.button("🔁 Recarregar Tela", use_container_width=True):

        st.cache_data.clear()
        st.rerun()


st.divider()


# =========================
# VERIFICAÇÃO DOS DADOS
# =========================

if not DATA_PATH.exists():

    st.warning(
        "Nenhum dataset processado encontrado. Clique em 'Atualizar Tudo' para gerar os dados."
    )

    st.stop()


df, network_summary, channel_summary, bssid_summary, anomalies_df = load_data()


# =========================
# MÉTRICAS PRINCIPAIS
# =========================

total_records = len(df)
unique_ssids = df["ssid"].nunique()
unique_bssids = df["bssid"].nunique()
avg_rssi = round(df["rssi"].mean(), 2)
best_rssi = int(df["rssi"].max())
worst_rssi = int(df["rssi"].min())
anomaly_count = len(anomalies_df)

st.subheader("📌 Visão Geral")

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Detecções", total_records)
col2.metric("SSIDs únicos", unique_ssids)
col3.metric("BSSIDs únicos", unique_bssids)
col4.metric("RSSI médio", f"{avg_rssi} dBm")
col5.metric("Melhor RSSI", f"{best_rssi} dBm")
col6.metric("Anomalias", anomaly_count)

st.divider()


# =========================
# FILTROS
# =========================

st.sidebar.header("Filtros")

ssid_filter = st.sidebar.multiselect(
    "SSID",
    options=sorted(df["ssid"].unique()),
    default=sorted(df["ssid"].unique())
)

channel_filter = st.sidebar.multiselect(
    "Canal",
    options=sorted(df["channel"].unique()),
    default=sorted(df["channel"].unique())
)

filtered_df = df[
    (df["ssid"].isin(ssid_filter))
    & (df["channel"].isin(channel_filter))
]


# =========================
# GRÁFICOS INTERATIVOS
# =========================

st.subheader("📈 RSSI ao longo do tempo")

st.line_chart(
    filtered_df,
    x="timestamp",
    y="rssi",
    color="ssid"
)

col_a, col_b = st.columns(2)

with col_a:

    st.subheader("📶 Redes mais detectadas")

    top_networks = (
        network_summary
        .sort_values("detections", ascending=False)
        .head(10)
        .set_index("ssid")
    )

    st.bar_chart(top_networks["detections"])

with col_b:

    st.subheader("📡 Distribuição por canal")

    channel_counts = (
        filtered_df["channel"]
        .value_counts()
        .sort_index()
    )

    st.bar_chart(channel_counts)


col_c, col_d = st.columns(2)

with col_c:

    st.subheader("⚡ Melhor sinal médio")

    strongest = (
        network_summary
        .sort_values("avg_rssi", ascending=False)
        .head(10)
        .set_index("ssid")
    )

    st.bar_chart(strongest["avg_rssi"])

with col_d:

    st.subheader("📉 Redes mais instáveis")

    unstable = (
        network_summary
        .sort_values("rssi_std", ascending=False)
        .head(10)
        .set_index("ssid")
    )

    st.bar_chart(unstable["rssi_std"])


st.divider()


# =========================
# BSSID / AP
# =========================

st.subheader("🧭 Inteligência por BSSID / AP")

col_e, col_f = st.columns(2)

with col_e:

    st.write("APs com maior presença")

    bssid_presence = (
        bssid_summary
        .sort_values("presence_score", ascending=False)
        .head(10)
    )

    st.dataframe(
        bssid_presence,
        use_container_width=True
    )

with col_f:

    st.write("APs mais estáveis")

    bssid_stability = (
        bssid_summary
        .sort_values("stability_score", ascending=False)
        .head(10)
    )

    st.dataframe(
        bssid_stability,
        use_container_width=True
    )


st.divider()


# =========================
# ANOMALIAS
# =========================

st.subheader("🚨 Anomalias")

if anomalies_df.empty:

    st.success("Nenhuma anomalia detectada.")

else:

    anomaly_counts = (
        anomalies_df["anomaly_type"]
        .value_counts()
    )

    st.bar_chart(anomaly_counts)

    st.dataframe(
        anomalies_df,
        use_container_width=True
    )


st.divider()


# =========================
# GALERIA DE GRÁFICOS GERADOS
# =========================

st.subheader("🖼️ Gráficos Gerados pelo Pipeline")

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Redes",
        "Canais",
        "BSSID",
        "Qualidade e Anomalias"
    ]
)

with tab1:

    show_image(
        Path("data/reports/top_networks.png"),
        "Top redes mais detectadas"
    )

    show_image(
        Path("data/reports/strongest_networks.png"),
        "Redes com melhor sinal médio"
    )

    show_image(
        Path("data/reports/most_unstable_networks.png"),
        "Redes mais instáveis"
    )

    show_image(
        Path("data/reports/rssi_timeline.png"),
        "RSSI ao longo do tempo"
    )

with tab2:

    show_image(
        Path("data/reports/channel_distribution.png"),
        "Distribuição por canal"
    )

    show_image(
        Path("data/reports/channel_load_score.png"),
        "Score de carga por canal"
    )

    show_image(
        Path("data/reports/avg_rssi_by_channel.png"),
        "RSSI médio por canal"
    )

with tab3:

    show_image(
        Path("data/reports/bssid_presence.png"),
        "Presença por BSSID/AP"
    )

    show_image(
        Path("data/reports/bssid_stability.png"),
        "Estabilidade por BSSID/AP"
    )

with tab4:

    show_image(
        Path("data/reports/anomaly_types.png"),
        "Tipos de anomalias"
    )

    show_image(
        Path("data/reports/quality_distribution.png"),
        "Distribuição de qualidade"
    )


st.divider()


# =========================
# TABELAS
# =========================

st.subheader("📋 Dados Processados")

st.dataframe(
    filtered_df,
    use_container_width=True
)

st.subheader("📊 Resumo por Rede")

st.dataframe(
    network_summary,
    use_container_width=True
)

st.subheader("📡 Resumo por Canal")

st.dataframe(
    channel_summary,
    use_container_width=True
)

st.subheader("🧭 Resumo por BSSID")

st.dataframe(
    bssid_summary,
    use_container_width=True
)