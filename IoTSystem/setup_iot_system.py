from typing import TYPE_CHECKING
from fastapi import Request

if TYPE_CHECKING: 
    from fastapi import FastAPI
    
def setup_iot_system(app: "FastAPI"):
    @app.get("/device_on")
    def device_on():
        
        return "Turned ON The Device"
    
    @app.get("/device_off")
    def device_off():
        return "Turned OFF The Device"