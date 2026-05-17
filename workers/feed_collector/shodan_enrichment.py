import requests
import os
from dotenv import load_dotenv

load_dotenv()

SHODAN_KEY = os.getenv("SHODAN_API_KEY")

def get_shodan_data(ip_address : str) -> dict:
    # Takes a IP address and returns the ports and services
    URL = f"https://api.shodan.io/shodan/host/{ip_address}"
    params = {
        "key": SHODAN_KEY
    } 

    response = requests.get(URL, params=params)

    if response.status_code == 404:
        return {
            "error": f"Error: IP address was not found"
        }
    elif response.status_code == 429:
        return {
            "error": f"Error: Rate limit hit"
        }
    else:
        data = response.json()
        
        return {
            "ip": data.get("ip_str"),
            "ports": data.get("ports", []),
            "org": data.get("org"),
            "country": data.get("country_name"),
            "city": data.get("city"),
            "hostname": data.get("hostnames", []),
            "data": str(data.get("data", [])[:1]),
            "timestamp": data.get("last_update")
        }


