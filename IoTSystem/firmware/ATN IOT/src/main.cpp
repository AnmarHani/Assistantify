#include <Arduino.h>
#include <WiFiManager.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>

// HiveMQ Cloud MQTT Broker settings
const char* MQTT_SERVER = "298321207d58431bb997da06e6cd2ca4.s1.eu.hivemq.cloud";
const char* MQTT_USERNAME = "ATN_IOT_SYSTEM";
const char* MQTT_PASSWORD = "Wasd1234";
const int MQTT_PORT = 8883; // Use port 8883 for secure connection (TLS/SSL)

// Initialize WiFi and MQTT clients
WiFiClientSecure espClient; // Secure client for TLS/SSL
PubSubClient client(espClient);

void setup_wifi() {
    // WiFiManager: Local initialization
    WiFiManager wm;

    // Optional: Reset WiFi credentials (for testing purposes)
    wm.resetSettings();

    // Try to auto-connect to WiFi, or start the access point for manual config
    if (!wm.autoConnect("ATN_IOT", "password")) {
        Serial.println("Failed to connect to WiFi, restarting...");
        ESP.restart();
    } else {
        Serial.println("Connected to WiFi");
    }
}

void reconnect() {
    // Loop until we're connected to the MQTT server
    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        // Attempt to connect
        if (client.connect("ESP8266Client", MQTT_USERNAME, MQTT_PASSWORD)) {
            Serial.println("Connected to MQTT broker");
            // Once connected, you can subscribe to topics here
            client.subscribe("ATN/led");
        } else {
            Serial.print("Failed: ");
            Serial.print(client.state());
            Serial.println(" trying again in 5 seconds");
            // Wait 5 seconds before retrying
            delay(5000);
        }
    }
}

void setup() {
    pinMode(D2, OUTPUT); // Set Pin D2 to output for LED control
    Serial.begin(115200);

    // Connect to WiFi
    setup_wifi();

    // Set the MQTT server and port
    client.setServer(MQTT_SERVER, MQTT_PORT);
    
    // Disable certificate verification (not secure, but simplifies testing)
    espClient.setInsecure(); 

    // Set callback function for handling messages
    client.setCallback([](char* topic, byte* payload, unsigned int length) {
        Serial.print("Message arrived in topic: ");
        Serial.println(topic);
        if (strncmp((char*)payload, "ON", length) == 0) {
            digitalWrite(D2, HIGH); // Turn LED on
        } else if (strncmp((char*)payload, "OFF", length) == 0) {
            digitalWrite(D2, LOW); // Turn LED off
        }
    });
}

void loop() {
    // Ensure the MQTT client stays connected
    if (!client.connected()) {
        reconnect();
    }

    // Handle incoming messages
    client.loop();
}
