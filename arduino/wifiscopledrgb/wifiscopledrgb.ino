#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecureBearSSL.h>

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// ======================
// WIFI
// ======================

const char* ssid = "RENAN";
const char* password = "renan456";

// ======================
// GOOGLE SHEETS
// ======================

String scriptURL = "https://script.google.com/macros/s/AKfycbzHfi1FhzYe7oamuLUrziR-TO7YTYwP6QxJ9vm68A9lgi7QfmgjsJggVKZtopCwKa9A3w/exec";

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
// LED RGB
// ======================

#define RGB_R_PIN D6
#define RGB_G_PIN D7
#define RGB_B_PIN D0

// Se as cores ficarem invertidas, troque para true
bool COMMON_ANODE = false;

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
// FUNCOES LED RGB
// ======================

void rgbWrite(bool r, bool g, bool b) {

  if (COMMON_ANODE) {
    r = !r;
    g = !g;
    b = !b;
  }

  digitalWrite(RGB_R_PIN, r ? HIGH : LOW);
  digitalWrite(RGB_G_PIN, g ? HIGH : LOW);
  digitalWrite(RGB_B_PIN, b ? HIGH : LOW);
}

void rgbOff() {
  rgbWrite(false, false, false);
}

void rgbBlue() {
  rgbWrite(false, false, true);
}

void rgbGreen() {
  rgbWrite(false, true, false);
}

void rgbYellow() {
  rgbWrite(true, true, false);
}

void rgbPurple() {
  rgbWrite(true, false, true);
}

void rgbRed() {
  rgbWrite(true, false, false);
}

void rgbWhite() {
  rgbWrite(true, true, true);
}

void blinkBlue() {

  rgbBlue();
  delay(250);

  rgbOff();
  delay(250);
}

// ======================
// FUNCOES GERAIS
// ======================

String getEncryptionType(int type) {

  if (type == ENC_TYPE_NONE) {
    return "OPEN";
  }

  return "SECURED";
}

String urlEncode(String str) {

  String encoded = "";
  char c;
  char code0;
  char code1;

  for (int i = 0; i < str.length(); i++) {

    c = str.charAt(i);

    if (isalnum(c)) {

      encoded += c;

    } else {

      code1 = (c & 0xf) + '0';

      if ((c & 0xf) > 9) {
        code1 = (c & 0xf) - 10 + 'A';
      }

      c = (c >> 4) & 0xf;

      code0 = c + '0';

      if (c > 9) {
        code0 = c - 10 + 'A';
      }

      encoded += '%';
      encoded += code0;
      encoded += code1;
    }
  }

  return encoded;
}

void showOLED() {

  rgbWhite();

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

  if (lastStatus == "Enviado" || lastStatus == "WiFi OK") {
    rgbGreen();
  } else if (lastStatus == "Erro HTTP" || lastStatus == "Erro HTTPS") {
    rgbRed();
  } else {
    rgbGreen();
  }
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

  pinMode(RGB_R_PIN, OUTPUT);
  pinMode(RGB_G_PIN, OUTPUT);
  pinMode(RGB_B_PIN, OUTPUT);

  rgbBlue();

  Wire.begin(D2, D1);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {

    Serial.println("Falha ao iniciar OLED");

    rgbRed();

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

    blinkBlue();

    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi conectado!");
  Serial.print("IP do ESP: ");
  Serial.println(WiFi.localIP());

  lastStatus = "WiFi OK";

  rgbGreen();
}

void loop() {

  checkButton();

  Serial.println();
  Serial.println("================================");
  Serial.println("NOVO SCAN WIFI");
  Serial.println("================================");

  rgbYellow();

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
      + "?ssid=" + urlEncode(ssidFound)
      + "&bssid=" + urlEncode(bssid)
      + "&rssi=" + String(rssi)
      + "&channel=" + String(channel)
      + "&encryption=" + urlEncode(encryption);

    std::unique_ptr<BearSSL::WiFiClientSecure> client(
      new BearSSL::WiFiClientSecure
    );

    client->setInsecure();

    HTTPClient https;

    Serial.println("Enviando para Google Sheets...");

    rgbPurple();

    if (https.begin(*client, url)) {

      int httpCode = https.GET();

      Serial.print("HTTP Code: ");
      Serial.println(httpCode);

      if (httpCode == 200 || httpCode == 302) {

        lastStatus = "Enviado";

        rgbGreen();

      } else {

        lastStatus = "Erro HTTP";

        rgbRed();
      }

      https.end();

    } else {

      Serial.println("Falha HTTPS");

      lastStatus = "Erro HTTPS";

      rgbRed();
    }

    checkButton();

    delay(1500);

    if (lastStatus == "Enviado") {
      rgbPurple();
    }
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

  if (lastStatus == "Enviado" || lastStatus == "WiFi OK") {
    rgbGreen();
  } else {
    rgbRed();
  }

  unsigned long startWait = millis();

  while (millis() - startWait < 300000) {

    checkButton();

    delay(100);
  }
}