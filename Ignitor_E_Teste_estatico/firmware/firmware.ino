// INCLUSÃO DE BIBLIOTECAS
#include <Wire.h>
#include <RTClib.h>
#include <HX711.h>
#include <FS.h>
#include <SD.h>
#include <SPI.h>
#include <Pushbutton.h>
#include <BluetoothSerial.h>
#include <esp_now.h>
#include <WiFi.h>

#include "Pressure.h"

// Definições de pinos e constantes
#define LED_PIN 4         // Pino do LED
#define CS_PIN 5          // Pino do cartão SD
#define BUZZER_PIN XX     // Pino do buzzer
#define BTN_PIN XX        // Pino do botão
#define ENC1_PIN XX       // Pino 1 do encoder
#define ENC2_PIN XX       // Pino 2 do encoder
#define CELULA_DT_PIN 26  // Pino de dados da célula de carga
#define CELULA_SCK_PIN 27 // Pino de clock da célula de carga
#define PRESSURE_PIN 34   // Pino do sensor de pressão
#define INTERVALO 100     // Precisão Leitura Dados milissegundos

// Variáveis globais
const float VinPressure = 5.0;    // Tensão que alimenta o sensor
const float VminPressure = 0.5;   // Tensão de saída em 0 MPa
const float VmaxPressure = 4.5;   // Tensão de saída em 10 MPa
const float maxPressure = 10.0;   // Pressão máxima do sensor em MPa
const float loadFactor = 277306;  // Valor encontrado na calibração
const float R1 = 10000.0;         // Resistor conectado entre o sensor e o pino do ESP32
const float R2 = 20000.0;         // Resistor conectado entre o pino do ESP32 e o GND
const int RESOLUCAO_ADC = 4095;   // ESP32 tem ADC de 12 bits (2^12 - 1)
const float TENSAO_MAX_ADC = 3.3; // Tensão de referência do ADC do ESP32
unsigned long previousMillis = 0; // Controle de tempo
bool selectLoop = false;          // Modo de operação
String dir = "";                  // Diretório
String filedir = "";              // Arquivo
String leitura = "";              // Leitura dos dados
bool espNowPeerReady = false;     // Estado do par ESP-NOW

// Configuração esp-now
uint8_t enderecoReceptor[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF}; // Endereço MAC do receptor

// Estrutura dos dados a serem enviados. Deve ser a mesma no transmissor e no receptor.
typedef struct struct_message
{
  char data[60]; // Array para armazenar a string de dados "Tempo,Empuxo"
} struct_message;

// Cria uma instância da estrutura e informações do par
struct_message minhaMensagem;
esp_now_peer_info_t peerInfo;

// Instanciação de objetos
Pushbutton button(BTN_PIN); // Botão
PressureSensor pressureSensor(PRESSURE_PIN, R1, R2, RESOLUCAO_ADC, TENSAO_MAX_ADC, VminPressure, VmaxPressure, maxPressure); // Sensor de pressão
RTC_DS3231 rtc;             // Relógio
HX711 escala;               // Célula de carga
BluetoothSerial SerialBT;   // Bluetooth

void setup()
{
  // Inicialização da comunicação serial
  Serial.begin(115200);
  SerialBT.begin("ESP32_BT");

  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(BTN_PIN, INPUT);

  setupESPNow();

  if (setupRTC() && setupSDCard() && setupHX711())
  {
    printToSerials("Sistema configurado. Transmitindo...");
    buzzSignal("Sucesso");
  }
  else
  {
    printToSerials("Falha crítica. Reiniciando...");
    buzzSignal("Alerta");
    delay(3000);
    ESP.restart();
  }
}

void loop()
{
  staticTest();
  if (button.getSingleDebounced())
  {
    buzzSignal("Beep");
    printToSerials("Célula Zerada!");
    escala.tare();
  }
}

// Função de callback ESP-NOW
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status)
{
  Serial.print("\r\nStatus do pacote ESP-NOW: ");
  if (status == ESP_NOW_SEND_SUCCESS)
  {
    Serial.println("Entrega com Sucesso");
  }
  else
  {
    Serial.println("Falha na Entrega");
  }
}

// Função para inicializar o ESP-NOW
void setupESPNow()
{
  WiFi.mode(WIFI_STA);
  if (esp_now_init() != ESP_OK)
  {
    Serial.println("ERRO CRÍTICO: Falha ao inicializar o ESP-NOW.");
    return; // Sai da função se a inicialização base falhar
  }

  esp_now_register_send_cb(OnDataSent);
  memcpy(peerInfo.peer_addr, enderecoReceptor, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;

  // ALTERADO: Tenta adicionar o par, mas não reinicia em caso de falha
  if (esp_now_add_peer(&peerInfo) != ESP_OK)
  {
    Serial.println("AVISO: Falha ao adicionar o par receptor. O ESP-NOW não transmitirá dados.");
    espNowPeerReady = false;
  }
  else
  {
    Serial.println("ESP-NOW OK! Par receptor adicionado com sucesso.");
    espNowPeerReady = true;
  }
}

// Sinalização com o buzzer
void buzzSignal(String signal)
{
  int frequency = 1000;   // Frequência do tom
  if (signal == "Alerta") // Alerta de erro em alguma configuração
  {
    for (int i = 0; i < 5; i++)
    {
      tone(BUZZER_PIN, frequency, 200);
      delay(200 + 150);
    }
  }
  else if (signal == "Sucesso") // Sinal de sucesso na configuração
  {
    for (int i = 0; i < 3; i++)
    {
      tone(BUZZER_PIN, frequency, 100);
      delay(100 + 100);
    }
  }
  else if (signal == "Ativado")
  {
    tone(BUZZER_PIN, frequency, 500);
  }
  else if (signal == "Beep") // Beep de funcionamento padrão
  {
    tone(BUZZER_PIN, frequency, 50);
  }
  else
  {
    Serial.println("Sinal inválido!");
  }
}

// Configuração do RTC
bool setupRTC()
{
  if (!rtc.begin())
  {
    printToSerials("DS3231 não encontrado");
    return false;
  }
  if (rtc.lostPower())
  {
    printToSerials("DS3231 OK!");
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
  return true;
}

// Recebe a data e hora atual formatada como String
String getCurrentDateTime()
{
  DateTime now = rtc.now();
  String data = "";

  data.concat(String(now.day(), DEC));
  data.concat('-');
  data.concat(String(now.month(), DEC));
  data.concat('-');
  data.concat(String(now.year(), DEC));
  data.concat('_');
  data.concat(String(now.hour(), DEC));
  data.concat('-');
  data.concat(String(now.minute(), DEC));
  data.concat('-');
  data.concat(String(now.second(), DEC));

  return data;
}

// Configuração do cartão SD e Arquivo
bool setupSDCard()
{
  if (!SD.begin(CS_PIN))
  {
    printToSerials("Falha no SD");
    return false;
  }
  if (SD.cardType() == CARD_NONE)
  {
    printToSerials("Cartão SD não encontrado");
    return false;
  }

  String now = getCurrentDateTime();
  dir = "/" + now;
  createDir(SD, dir);
  filedir = dir + "/" + now + "_raw.txt";
  if (writeFile(SD, filedir, "Tempo,Empuxo")) // Criação do arquivo para armazenamento de dados
  {
    printToSerials("Arquivo criado com sucesso");
    return true;
  }
  else
  {
    printToSerials("Falha ao criar arquivo");
    return false;
  }
}

// Configuração da célula de carga HX711
bool setupHX711()
{
  escala.begin(CELULA_DT_PIN, CELULA_SCK_PIN);
  escala.set_scale(loadFactor);
  escala.tare();
  if (escala.is_ready())
  {
    printToSerials("HX711 conectado");
    return true;
  }
  else
  {
    printToSerials("HX711 não encontrado");
    return false;
  }
}

// Função para registrar e imprimir os dados do momento
// Formato: Tempo (ms), Empuxo (Kg), Pressão (MPa)
void logData(unsigned long millis)
{
  float peso = escala.get_units();
  float pressao = pressureSensor.readMPa(); 
  leitura = String(millis) + "," + String(peso, 3) + "," + String(pressao, 3);
  printToSerials(leitura);
  appendFile(SD, filedir, leitura);
}

// Escrita de dados em um arquivo
bool writeFile(fs::FS &fs, String path, String message)
{
  File file = fs.open(path, FILE_WRITE);
  if (!file)
  {
    printToSerials("Falha ao abrir o arquivo");
    return false;
  }
  if (file.print(message))
  {
    digitalWrite(LED_PIN, HIGH);
  }
  else
  {
    printToSerials("Falha ao escrever no arquivo - w");
    digitalWrite(LED_PIN, LOW);
    return false;
  }
  file.close();
  return true;
}

// Anexação de dados em um arquivo
void appendFile(fs::FS &fs, const String &path, const String &message)
{
  // Adição de dados em um arquivo
  File file = fs.open(path, FILE_APPEND);
  if (!file)
  {
    printToSerials("Falha ao abrir o arquivo");
  }
  if (file.print(message + "\n"))
  {
    digitalWrite(LED_PIN, HIGH);
  }
  else
  {
    printToSerials("Falha ao escrever no arquivo - a");
    digitalWrite(LED_PIN, LOW);
  }
  file.close();
}

// Criação de diretório
void createDir(fs::FS &fs, const String &path)
{
  if (fs.mkdir(path))
  {
    printToSerials("Dir created");
  }
  else
  {
    printToSerials("mkdir failed");
  }
}

// Função para imprimir na Serial e SerialBT
void printToSerials(const String &message)
{
  // Serial monitor
  Serial.println(message);

  // Serial Bluetooth
  SerialBT.println(message);

  // Envio via ESP-NOW
  if (espNowPeerReady)
  {
    message.toCharArray(minhaMensagem.data, sizeof(minhaMensagem.data));
    esp_err_t result = esp_now_send(enderecoReceptor, (uint8_t *)&minhaMensagem, sizeof(minhaMensagem));

    if (result != ESP_OK)
    {
      Serial.println("ESP-NOW: Erro ao enfileirar pacote para envio.");
    }
  }
}

// Função de teste estático
void staticTest()
{
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis > INTERVALO)
  {
    logData(currentMillis);
    previousMillis = currentMillis;
  }
}