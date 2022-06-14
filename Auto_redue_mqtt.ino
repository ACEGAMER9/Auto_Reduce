#include <ESP8266WiFi.h>
#include <PubSubClient.h>

//--define WiFi information.
const char* ssid = "AAA";
const char* password = "ace12344";

//--define MQTT information.
const char* mqtt_server = "broker.hivemq.com";
const char* mqtt_user = "";
const char* mqtt_password = "";
const int mqtt_port = 1883;

//--define Thing's name
#define ALIAS "node_Auto_redue"

WiFiClient ethClient;
PubSubClient client(mqtt_server,mqtt_port,ethClient);

//call back function
void doSubscribe(char* topic, byte* payload, unsigned int length){
  char strState[length];// declear array size of length.
  for(int i=0;i<length;i++){
    strState[i] = (char)payload[i];
    if(strState[i] == '1'){
       Serial.print(strState[i]);
       digitalWrite(D1, HIGH);
       delay(1000);  
     }
    else if(strState[i] == '2'){
       Serial.print(strState[i]);
       digitalWrite(D2, HIGH);
       delay(1000);  
     }
    else if(strState[i] == '3'){
       Serial.print(strState[i]);
       digitalWrite(D3, HIGH);
       delay(1000); 
     }
    else if(strState[i] == '4'){
       Serial.print(strState[i]);
       digitalWrite(D4, HIGH);
       delay(1000); 
     }
    else if(strState[i] == '0'){
       Serial.print(strState[i]);
       digitalWrite(D1, LOW);
       digitalWrite(D2, LOW);
       digitalWrite(D3, LOW);
       digitalWrite(D4, LOW);
       delay(1000);
     }
    else if(strState[i] == '9'){
       digitalWrite(D1, HIGH);
       digitalWrite(D2, HIGH);
       digitalWrite(D3, HIGH);
       digitalWrite(D4, HIGH);
       delay(1000);
     }
  }
  Serial.println();
  String stateStr = String(strState).substring(0,length);
  String head = String(strState).substring(0,1);
}

//user defined function
void reconnect(){
    while(!client.connected()){
    if(client.connect(ALIAS,mqtt_user,mqtt_password)){
      Serial.println("MQTT has connected...");
      client.subscribe("/auto_redue/mqtt/control/motor");
    }else{
      Serial.print("Fail to connect, Error ");Serial.println(client.state());
    }
  }
}


void setup() {
  pinMode(D1, OUTPUT);
  pinMode(D2, OUTPUT);
  pinMode(D3, OUTPUT);
  pinMode(D4, OUTPUT);
  
  // put your setup code here, to run once:
  Serial.begin(9600);
  //setup WiFi
  WiFi.begin(ssid,password);
  while(WiFi.status() != WL_CONNECTED){
    Serial.print(".");
    delay(500);
  }
  Serial.println("WiFi has connected....");
  Serial.print("IP Address:");Serial.println(WiFi.localIP());

  //setup MQTT
  client.setServer(mqtt_server,mqtt_port);
  client.setCallback(doSubscribe);
  
  reconnect();
}

void loop() {
  // put your main code here, to run repeatedly:
  if(!client.connected()){
    reconnect();
  }
  client.loop(); //interact to server, tell server, it still alive.

  delay(3000);

}
