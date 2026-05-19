#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecureBearSSL.h>

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// ======================
// WIFI
// ======================

const char* ssid = "******";
const char* password = "******";

// ======================
// GOOGLE SHEETS
// ======================

String scriptURL = "*******";

// ======================
// OLED
// ======================

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(
  SCREEN_WIDTH,
  SCREEN_HEIGHT,
  &Wire,
  -1
);

// ======================
// BOTAO
// ======================

#define BUTTON_PIN D5

// ======================
// DADOS DO ULTIMO SCAN
// ======================

int lastNetworks = 0;
int lastBestRSSI = -100;
int lastWorstRSSI = 0;
int lastAverageRSSI = 0;
int lastBusyChannel = 0;
String lastStrongestSSID = "";
String lastStatus = "Aguardando";

unsigned long lastButtonPress = 0;

// ======================
// FUNCOES
// ======================

String getEncryptionType(int type) {

  if (type == ENC_TYPE_NONE) {
    return "OPEN";
  }

  return "SECURED";
}

void showOLED() {

  display.ssd1306_command(SSD1306_DISPLAYON);

  display.clearDisplay();

  display.setTextColor(WHITE);
  display.setTextSize(1);

  display.setCursor(0, 0);
  display.println("WiFi Intelligence");

  display.setCursor(0, 12);
  display.print("Redes: ");
  display.println(lastNetworks);

  display.setCursor(0, 24);
  display.print("Melhor: ");
  display.print(lastBestRSSI);
  display.println(" dBm");

  display.setCursor(0, 36);
  display.print("Media: ");
  display.print(lastAverageRSSI);
  display.println(" dBm");

  display.setCursor(0, 48);
  display.print("Canal: ");
  display.print(lastBusyChannel);
  display.print(" ");
  display.println(lastStatus);

  display.display();

  delay(8000);

  display.clearDisplay();
  display.display();

  display.ssd1306_command(SSD1306_DISPLAYOFF);
}

void checkButton() {

  if (digitalRead(BUTTON_PIN) == LOW) {

    if (millis() - lastButtonPress > 800) {

      lastButtonPress = millis();

      showOLED();
    }
  }
}

void setup() {

  Serial.begin(115200);

  pinMode(BUTTON_PIN, INPUT_PULLUP);

  Wire.begin(D2, D1);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {

    Serial.println("Falha ao iniciar OLED");

    while (true);
  }

  display.clearDisplay();
  display.display();
  display.ssd1306_command(SSD1306_DISPLAYOFF);

  WiFi.mode(WIFI_STA);

  WiFi.begin(ssid, password);

  Serial.println();
  Serial.println("Conectando ao WiFi...");

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi conectado!");
  Serial.print("IP do ESP: ");
  Serial.println(WiFi.localIP());

  lastStatus = "WiFi OK";
}

void loop() {

  checkButton();

  Serial.println();
  Serial.println("================================");
  Serial.println("NOVO SCAN WIFI");
  Serial.println("================================");

  int n = WiFi.scanNetworks();

  lastNetworks = n;

  int somaRSSI = 0;
  int canalCount[14] = {0};

  lastBestRSSI = -100;
  lastWorstRSSI = 0;
  lastStrongestSSID = "";

  Serial.print("Redes encontradas: ");
  Serial.println(n);

  for (int i = 0; i < n; i++) {

    String ssidFound = WiFi.SSID(i);
    String bssid = WiFi.BSSIDstr(i);
    int rssi = WiFi.RSSI(i);
    int channel = WiFi.channel(i);
    String encryption = getEncryptionType(WiFi.encryptionType(i));

    somaRSSI += rssi;

    if (rssi > lastBestRSSI) {
      lastBestRSSI = rssi;
      lastStrongestSSID = ssidFound;
    }

    if (rssi < lastWorstRSSI) {
      lastWorstRSSI = rssi;
    }

    if (channel >= 1 && channel <= 13) {
      canalCount[channel]++;
    }

    Serial.println();
    Serial.print("SSID: ");
    Serial.println(ssidFound);

    Serial.print("BSSID: ");
    Serial.println(bssid);

    Serial.print("RSSI: ");
    Serial.println(rssi);

    Serial.print("Canal: ");
    Serial.println(channel);

    Serial.print("Criptografia: ");
    Serial.println(encryption);

    String url =
      scriptURL
      + "?ssid=" + ssidFound
      + "&bssid=" + bssid
      + "&rssi=" + String(rssi)
      + "&channel=" + String(channel)
      + "&encryption=" + encryption;

    std::unique_ptr<BearSSL::WiFiClientSecure> client(
      new BearSSL::WiFiClientSecure
    );

    client->setInsecure();

    HTTPClient https;

    Serial.println("Enviando para Google Sheets...");

    if (https.begin(*client, url)) {

      int httpCode = https.GET();

      Serial.print("HTTP Code: ");
      Serial.println(httpCode);

      if (httpCode == 200 || httpCode == 302) {
        lastStatus = "Enviado";
      } else {
        lastStatus = "Erro HTTP";
      }

      https.end();

    } else {

      Serial.println("Falha HTTPS");

      lastStatus = "Erro HTTPS";
    }

    checkButton();

    delay(1500);
  }

  if (n > 0) {
    lastAverageRSSI = somaRSSI / n;
  } else {
    lastAverageRSSI = 0;
  }

  int maiorCongestionamento = 0;
  lastBusyChannel = 0;

  for (int ch = 1; ch <= 13; ch++) {

    if (canalCount[ch] > maiorCongestionamento) {

      maiorCongestionamento = canalCount[ch];
      lastBusyChannel = ch;
    }
  }

  Serial.println();
  Serial.println("========== RESUMO ==========");
  Serial.print("Redes: ");
  Serial.println(lastNetworks);

  Serial.print("Melhor RSSI: ");
  Serial.println(lastBestRSSI);

  Serial.print("RSSI medio: ");
  Serial.println(lastAverageRSSI);

  Serial.print("Canal mais usado: ");
  Serial.println(lastBusyChannel);

  Serial.print("Rede mais forte: ");
  Serial.println(lastStrongestSSID);

  Serial.print("Status: ");
  Serial.println(lastStatus);

  Serial.println();
  Serial.println("Aguardando 5 minutos...");

  unsigned long startWait = millis();

  while (millis() - startWait < 300000) {

    checkButton();

    delay(100);
  }
}