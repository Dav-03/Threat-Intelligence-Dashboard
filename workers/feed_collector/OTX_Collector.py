import os 
from dotenv import load_dotenv
from OTXv2 import OTXv2
from datetime import datetime


load_dotenv()
OTX = os.getenv("OTX_API_KEY")

otx_Key = OTXv2(OTX)

def get_OTX_data():
    # Returns a list of raw IoC's by looping through the atest pulses
    ioc_rows = []
    Pulse_List = otx_Key.getall(limit=10)

    for pulse in Pulse_List:
        source = pulse.get("name", "AlienVault OTX")
        severity = pulse.get("TLP", "white")
        timestamp = datetime.fromisoformat(pulse.get("modified")) if pulse.get("modified") else datetime.now()

        indicators = pulse.get("indicators", [])

        for indicator in indicators:
            ioc = {
                "type": indicator.get("type"),
                "value": indicator.get("indicator"),
                "source": source,
                "severity": severity,
                "timestamp": timestamp
            }

            ioc_rows.append(ioc)
    
    return ioc_rows
