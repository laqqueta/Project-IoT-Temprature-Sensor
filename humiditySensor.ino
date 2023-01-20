#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

#define LED D5
#define DHTPIN D1
#define DHTTYPE DHT11

#define WIFI_SSID "asramastikom"
#define WIFI_PASSWORD "asramastikom"

#define MQTT_SERVER "192.168.18.173"
#define MQTT_PORT 1883
#define MQTT_USER "mbkm"
#define MQTT_PASS "mbkm"

#define MQTT_TOPIC_PUBLISH "device/room/kitchen/"
#define MQTT_TOPIC_SUBCRIBE "device/room/kitchen/"

DHT dht(DHTPIN, DHTTYPE); 
WiFiClient espClient;
PubSubClient client(espClient);

void connectToWifi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(350);
  }
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());
}

void reconnectToMqtt() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "Gamzv - IoT Device";
    
    if (client.connect(clientId.c_str(),MQTT_USER,MQTT_PASS)) {
      Serial.println("connected   ");
      client.publish("device/room/kitchen/", "Gamzv user connected");
      client.subscribe(MQTT_TOPIC_SUBCRIBE);
    } else { 
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setupLamp(char* topic, byte *payload) {
  if(topic=="MQTT_SERIAL_RECEIVER_CH") {
    digitalWrite(LED,atoi((char *)payload)); 
  }
}

void callback(char* topic, byte *payload, unsigned int length) {
  Serial.println("-------new message from broker-----");
  Serial.print("channel:");
  Serial.println(topic);
  Serial.print("data:"); 
  Serial.write(payload, length);
  Serial.println();

  setupLamp(topic,payload);
}
      
void publishSerialData(char *serialData){
  if (!client.connected()) {
    reconnectToMqtt();
  }
  client.publish(MQTT_TOPIC_PUBLISH, serialData);
}
          
void setup() {
  Serial.begin(9600);
  dht.begin();
  connectToWifi();
  client.setServer(MQTT_SERVER, MQTT_PORT);
  client.setCallback(callback);
  reconnectToMqtt();
  pinMode(LED, OUTPUT);
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  
  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print("\n");
  Serial.print(F(" Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));
  
  String message = String(t) + ":" + String(h);
  
  client.loop();
  client.publish(MQTT_TOPIC_PUBLISH, message.c_str());
  delay(1000);

  if (Serial.available() > 0) {
    char bfr[101];
    memset(bfr,0, 101);
    Serial.readBytesUntil( '\n',bfr,100);
    publishSerialData(bfr);
  }
}