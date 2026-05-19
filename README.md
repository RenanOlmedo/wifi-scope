# 📡 WiFi Scope

Wireless Intelligence Platform using ESP8266, Google Sheets, Python Analytics and Streamlit Dashboard.

---

# 🚀 Overview

WiFi Scope is a modular wireless monitoring and RF analytics platform designed to collect, analyze and visualize Wi-Fi environment data in real time.

The system combines:

- ESP8266 IoT scanning
- Google Sheets cloud ingestion
- Python analytics pipeline
- Streamlit dashboard
- Automated DOCX technical reports

The project focuses on wireless observability, RF behavior analysis and automated intelligence generation.

---

# 🧠 Main Features

## 📡 ESP8266 Wireless Scanner

- Wi-Fi scanning
- RSSI collection
- BSSID identification
- Channel detection
- Encryption analysis
- OLED display support
- Physical button interaction
- Portable operation using hotspot or local Wi-Fi

---

## ☁️ Cloud Data Collection

Data is sent automatically to Google Sheets using Google Apps Script as a lightweight cloud backend.

Collected fields:

| Field | Description |
|---|---|
| timestamp | Detection timestamp |
| ssid | Wi-Fi network name |
| bssid | Physical AP identifier |
| rssi | Signal strength |
| channel | Wi-Fi channel |
| encryption | Security type |

---

# 🧪 Python Analytics Pipeline

The analytics engine performs:

- data collection
- data cleaning
- feature engineering
- signal classification
- network analysis
- BSSID/AP analysis
- channel analysis
- anomaly detection
- RF stability analysis

---

# 📊 Visual Analytics

Automatically generated charts:

- top detected networks
- strongest networks
- most unstable networks
- channel distribution
- RSSI timeline
- channel load score
- average RSSI by channel
- BSSID presence
- BSSID stability
- anomaly distribution
- signal quality distribution

---

# 🖥️ Streamlit Dashboard

Interactive dashboard with:

- live metrics
- filters
- interactive charts
- anomaly visualization
- AP intelligence tables
- report generation
- project control center

Dashboard controls:

- Update pipeline
- Generate DOCX report
- Open reports folder
- Open processed datasets
- Open generated charts
- Reload dashboard

---

# 📄 Automated Technical Reports

WiFi Scope automatically generates professional DOCX reports including:

- dynamic technical explanations
- RF interpretation
- embedded charts
- wireless intelligence insights
- anomaly analysis
- signal quality evaluation
- channel occupancy analysis

Reports are timestamped and organized automatically.

---

# 🏗️ Project Architecture

```text
ESP8266
   ↓
Google Sheets
   ↓
Python Analytics Pipeline
   ↓
Charts + RF Intelligence + DOCX Reports
   ↓
Streamlit Dashboard


📂 Project Structure
wifi_scope/
│
├── analytics/
├── arduino/
├── collector/
├── dashboard/
├── processing/
├── reporting/
├── visualization/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── reports/
│
├── config.py
├── main.py
├── requirements.txt
└── README.md
⚙️ Technologies Used
Hardware
ESP8266 NodeMCU
SSD1306 OLED Display
Push Button
Software
Python
Pandas
Matplotlib
Streamlit
Google Sheets
Google Apps Script
python-docx
📈 Wireless Intelligence Capabilities

WiFi Scope can identify:

dominant access points
channel congestion
unstable networks
temporary networks
RF anomalies
signal quality patterns
AP stability behavior
temporal RSSI variations
🔮 Future Improvements
predictive analytics
RF heatmaps
AI-based environment classification
real-time alerts
SQL backend
online deployment
wireless threat detection


👨‍💻 Author

Renan Ferreira

GitHub:
https://github.com/RenanOlmedo

📜 License

This project is open-source and available for educational and research purposes.