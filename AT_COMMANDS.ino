#include <SoftwareSerial.h>

//Create software serial object to communicate with SIM800L
SoftwareSerial mySerial(3, 2); //SIM800L Tx & Rx is connected to Arduino #3 & #2

void setup()
{
  //Begin serial communication with Arduino and Arduino IDE (Serial Monitor)
  Serial.begin(9600);
  
  //Begin serial communication with Arduino and SIM800L
  mySerial.begin(9600);

  Serial.println("Iniciando programa...");
  delay(1000);

  mySerial.println("AT"); //Once the handshake test is successful, it will back to OK
  updateSerial();

  // Signal quality test (0-31)
  mySerial.println("AT+CSQ"); 
  updateSerial();

  //Read SIM information to confirm whether the SIM is plugger
  mySerial.println("AT+CCID"); 
  updateSerial();

  // Request TA serial number identification (IMEI)
  mySerial.println("AT+GSN"); 
  updateSerial(); 

  // Request if PIN is necessary
  //mySerial.println("AT+CPIN?"); 
  //updateSerial(); 

  //SIM PIN is given
  //mySerial.println("AT+CPIN=\"8462\"");
  //updateSerial(); 

  //Register in the network
  mySerial.println("AT+CREG=1"); 
  updateSerial();

  //Check whether it has registered in the network
  mySerial.println("AT+CREG?"); 
  updateSerial();


}

void loop()
{
  updateSerial();
}

void updateSerial()
{
  delay(500);
  while (Serial.available()) 
  {
    mySerial.write(Serial.read());//Forward what Serial received to Software Serial Port
  }
  while(mySerial.available()) 
  {
    Serial.write(mySerial.read());//Forward what Software Serial received to Serial Port
  }
}