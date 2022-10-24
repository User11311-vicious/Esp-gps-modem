#include "BluetoothSerial.h"
 
BluetoothSerial SerialBT;

const int stop_verh = 32;
const int stop_niz = 33;
const int gaz_verh = 25;
const int gaz_niz = 26;

void setup() {

  Serial.begin(115200);
  SerialBT.begin("ESP32");
  pinMode(stop_verh, INPUT);
  pinMode(stop_niz, INPUT);
  pinMode(gaz_verh, INPUT);
  pinMode(gaz_niz, INPUT);

  Serial.println("Let's gooo!!!");
}

void loop() {
  SerialBT.println("Hello World");
  bool bool_stop_verh = digitalRead(stop_verh);
  bool bool_stop_niz = digitalRead(stop_niz);
  bool bool_gaz_verh = digitalRead(gaz_verh);
  bool bool_gaz_niz = digitalRead(gaz_niz);
  SerialBT.print("STOP get ready: ");SerialBT.print(bool_stop_verh);SerialBT.print(" | ");
  SerialBT.print("STOP pressed: ");SerialBT.print(bool_stop_niz);SerialBT.println();
  SerialBT.print("GAZ get ready: ");SerialBT.print(bool_gaz_verh);SerialBT.print(" | ");
  SerialBT.print("GAZ pressed: ");SerialBT.print(bool_gaz_niz);SerialBT.println();

  delay(1000);
}


