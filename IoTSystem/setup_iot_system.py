from typing import TYPE_CHECKING
from fastapi import Request
import time
import broadlink
import paho.mqtt.client as paho
from paho import mqtt
import ssl

if TYPE_CHECKING:
    from fastapi import FastAPI

is_broadlink_enabled = True
is_slides_enabled = False
is_IOT_enabled = False

if is_slides_enabled:
    # Change the SSID and Password of your WiFi Network
    broadlink.setup('TAHMAL', "*cB222333", 4)
    LEFT_SLIDE_IR_CODE = b''
    RIGHT_SLIDE_IR_CODE = b''

if is_broadlink_enabled:
    # Change the SSID and Password of your WiFi Network
    broadlink.setup('SEC3', "SEC232323", 4)

    TURN_ON_BLITZ = b'&\x00`\x00\x00\x01!\x8e\x135\x13\x11\x12\x12\x13\x11\x13\x11\x13\x11\x12\x12\x12\x11\x13\x11\x135\x135\x125\x135\x125\x144\x135\x125\x135\x135\x13\x11\x12\x12\x12\x11\x13\x11\x13\x11\x12\x12\x13\x11\x13\x11\x134\x135\x125\x145\x125\x13\x00\x04\xfc\x00\x01 G\x13\x00\x0b\xfa\x00\x01!G\x13\x00\x0b\xfa\x00\x01!F\x13\x00\r\x05'
    TURN_OFF_BLITZ = b'&\x00X\x00\x00\x01\x1f\x91\x116\x11\x13\x11\x13\x11\x12\x12\x12\x11\x13\x12\x13\x11\x12\x12\x12\x116\x126\x117\x126\x116\x116\x127\x116\x126\x116\x11\x14\x11\x13\x11\x12\x12\x12\x11\x13\x11\x13\x11\x12\x12\x13\x116\x126\x116\x126\x117\x11\x00\x04\xfe\x00\x01\x1eI\x12\x00\x0b\xfb\x00\x01 H\x11\x00\r\x05'
    START_BLITZ = b'&\x00H\x00\x00\x01\x1f\x91\x125\x12\x12\x11\x13\x11\x12\x12\x12\x12\x12\x11\x14\x11\x12\x12\x12\x125\x126\x117\x126\x116\x116\x127\x11\x13\x11\x12\x126\x11\x13\x11\x12\x12\x13\x11\x13\x11\x13\x116\x116\x12\x12\x117\x126\x116\x126\x117\x11\x00\r\x05'
    BACK_TO_BASE_BLITZ = b'&\x00P\x00\x00\x01 \x8f\x135\x13\x11\x12\x11\x13\x11\x13\x11\x14\x11\x12\x11\x13\x11\x13\x11\x134\x135\x135\x134\x135\x126\x135\x12\x11\x135\x12\x11\x13\x11\x14\x11\x13\x11\x12\x12\x12\x11\x135\x12\x11\x145\x125\x134\x135\x144\x135\x12\x00\x04\xfc\x00\x01!G\x12\x00\r\x05'

    try:
        devices = broadlink.discover(timeout=10)
        print(devices)
        device = devices[0]
        device.auth()
    except:
        print("No devices found")
        exit()

    def learn_ir_code():
        device.enter_learning()
        start = time.time()
        while time.time() - start < 20:
            time.sleep(1)
            try:
                data = device.check_data()
                if data:
                    return data
            except:
                print("No data received")
    # device.send_data(PACKET)
    # print("Learning IR Code " + str(learn_ir_code()))


if is_IOT_enabled:
    print("OK?")
    # setting callbacks for different events to see if it works, print the message etc.

    def on_connect(client, userdata, flags, rc, properties=None):
        print("CONNACK received with code %s." % rc)

    # userdata is user defined data of any type, updated by user_data_set()
    # client_id is the given name of the client
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    client.on_connect = on_connect

    # enable TLS for secure connection
    # client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    # client.tls_set(tls_version=ssl.PROTOCOL_TLS)
    client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
    # set username and password
    client.username_pw_set("ATN_IOT_SYSTEM", "Wasd1234")
    # connect to HiveMQ Cloud on port 8883 (default for MQTT)
    client.connect("298321207d58431bb997da06e6cd2ca4.s1.eu.hivemq.cloud", 8883)
    client.loop_start()


def setup_iot_system(app: "FastAPI"):
    if is_slides_enabled:
        @app.get("/TURN_LEFT_SLIDE")
        def turn_left_slide():
            device.send_data(LEFT_SLIDE_IR_CODE)
            return "Turned Slide Left"

        @app.get("/TURN_RIGHT_SLIDE")
        def turn_right_slide():
            device.send_data(RIGHT_SLIDE_IR_CODE)
            return "Turned Slide Right"

    if is_broadlink_enabled:
        @app.get("/device_on")
        def blitz_on():
            device.send_data(TURN_ON_BLITZ)
            time.sleep(5)
            device.send_data(START_BLITZ)
            return "Turned ON The Device"

        @app.get("/device_off")
        def blitz_off():
            device.send_data(BACK_TO_BASE_BLITZ)
            time.sleep(15)
            device.send_data(TURN_OFF_BLITZ)
            return "Turned OFF The Device"

    if is_IOT_enabled:
        @app.get("/LED_ON")
        def turn_LED_ON():
            client.publish("ATN/led", payload="ON", qos=1)
            return "Sent!"

        @app.get("/LED_OFF")
        def turn_LED_ON():
            client.publish("ATN/led", payload="OFF", qos=1)
            return "Sent!"
