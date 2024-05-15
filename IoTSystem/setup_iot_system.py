from typing import TYPE_CHECKING
from fastapi import Request
import time
import broadlink

if TYPE_CHECKING:
    from fastapi import FastAPI


# Change the SSID and Password of your WiFi Network
broadlink.setup('TAHMAL', "*cB222333", 4)
TURN_ON = b'&\x00@\x00\x00\x01\r\x8a\x103\x10\x12\x10\x12\x0f\x14\x0e4\x11\x11\x0f\x13\x0e\x14\x0f\x12\x0f\x13\x0f\x13\x0f\x14\x0e\x12\x0f\x13\x0f\x12\x10\x12\x0f4\x10\x12\x0f4\x103\x10\x12\x0f4\x10\x12\x0f4\x10\x12\x0f\x13\x0f\x12\x10\x12\x0f\x00\r\x05'
TURN_OFF = b'&\x00@\x00\x00\x01\x10\x87\x122\x12\x10\x11\x11\x11\x10\x121\x13\x0f\x12\x10\x12\x10\x121\x130\x13\x10\x12\x10\x11\x11\x11\x10\x12\x10\x11\x11\x11\x10\x12\x10\x12\x10\x11\x11\x11\x10\x121\x12\x10\x121\x12\x10\x12\x10\x11\x11\x112\x12\x00\r\x05'

# devices = broadlink.discover(timeout=5)
# device = devices[0]
# device.auth()


def learn_ir_code():
    start = time.time()
    while time.time() - start < 20:
        time.sleep(1)
        try:
            data = device.check_data()
        except:
            print("No data received")
            return
        else:
            return data


def setup_iot_system(app: "FastAPI"):
    @app.get("/device_on")
    def device_on():
        device.send_data(TURN_ON)
        return "Turned ON The Device"

    @app.get("/device_off")
    def device_off():
        device.send_data(TURN_OFF)
        return "Turned OFF The Device"
