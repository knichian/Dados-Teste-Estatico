// INCLUSÃO DE BIBLIOTECAS
#include <Wire.h>
#include "RTClib.h"
#include "HX711.h"
#include "FS.h"
#include "SD.h"
#include "SPI.h"
#include <Pushbutton.h>
#include "BluetoothSerial.h"

// INCLUSÃO DE CÓDIGOS
// #include "Calibrar.h" 

// Definições de pinos e constantes
#define LED_PIN 4         // Pino do LED
#define CS_PIN 5          // Pino do cartão SD
#define BUZZER_PIN XX     // Pino do buzzer
#define JUMPER_PIN XX     // Pino do jumper
#define SELECT_PIN XX     // Pino de seleção de modo
#define BTN_PIN XX        // Pino do botão
#define ENC1_PIN XX       // Pino 1 do encoder
#define ENC2_PIN XX       // Pino 2 do encoder
#define CELULA_DT_PIN 26  // Pino de dados da célula de carga
#define CELULA_SCK_PIN 27 // Pino de clock da célula de carga
#define INTERVALO 100     // Precisão Leitura Dados milissegundos

// Instanciação de objetos
Pushbutton button(BTN_PIN); // Botão
RTC_DS3231 rtc;             // Relógio
HX711 escala;               // Célula de carga
BluetoothSerial SerialBT;   // Bluetooth

// Variáveis globais
const float loadFactor = 277306;  // Valor encontrado na calibração
unsigned long previousMillis = 0; // Controle de tempo
bool selectLoop = false;          // Modo de operação
String dir = "";                  // Diretório
String filedir = "";              // Arquivo
String leitura = "";              // Leitura dos dados

void setup()
{
  // Inicialização da comunicação serial
  Serial.begin(115200);
  SerialBT.begin("ESP32_BT");

  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(BTN_PIN, INPUT);
  pinMode(SELECT_PIN, INPUT_PULLUP);
  pinMode(JUMPER_PIN, INPUT_PULLUP);

  if (digitalRead(JUMPER_PIN) == HIGH)
  {
    printToSerials("Modo de Configuração Ativado");
    buzzSignal("Ativado");
  }
  else
  {
    selectLoop = digitalRead(SELECT_PIN) == HIGH;
    if (selectLoop)
    {
      if (setupRTC() && setupSDCard() && setupHX711())
      {
        printToSerials("Teste estático.");
        buzzSignal("Sucesso");
      }
      else
      {
        ESP.restart();
      }
    }
    else
    {
      printToSerials("Mostrando dados.");
    }
  }
}

void loop()
{
  estatico();
  if (button.getSingleDebounced())
  {
    buzzSignal("Beep");
    printToSerials("Célula Zerada!");
    escala.tare();
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
  data.concat(';');
  data.concat(String(now.hour(), DEC));
  data.concat(':');
  data.concat(String(now.minute(), DEC));
  data.concat(':');
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
void setupHX711()
{
  escala.begin(CELULA_DT_PIN, CELULA_SCK_PIN);
  escala.set_scale(loadFactor);
  escala.tare();
}

// Função para registrar e imprimir os dados do momento
// Formato: Empuxo (kg), Tempo (ms)
void logData(unsigned long millis)
{
  float peso = escala.get_units();
  leitura = String(peso, 3) + "," + String(millis);
  printtoSerials(leitura);
  appendFile(SD, filedir, leitura, 'a');
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
  Serial.println(message);
  SerialBT.println(message);
}

void estatico()
{
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis > INTERVALO)
  {
    logData(currentMillis);
    previousMillis = currentMillis;
  }
}