import os
from dotenv import load_dotenv
import requests

load_dotenv()

VIRUS_TOTAL_KEY = os.getenv("VIRUSTOTAL_API_KEY")


def check_ip(ip_Address: str) -> dict:
    # Takes a single IoC value so a IP or Hash and returns a score of that value
    URL = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_Address}"
    
    headers = {
        "accept": "application/json",
        "x-apikey": VIRUS_TOTAL_KEY
    }

    response = requests.get(URL, headers=headers)

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
        stats = data["data"]["attributes"]["last_analysis_stats"]
        attributes = data["data"]["attributes"]

        return {
            "ip": ip_Address,
            "malicious": stats["malicious"],
            "detection_ratio": f"{stats['malicious']}/{sum(stats.values())}",
            "country": attributes.get("country", "unknown"),
            "asn": attributes.get("asn", "unknown"),
            "as_owner": attributes.get("as_owner", "unknown"),
            "reputation": attributes.get("reputation", "unknown"),
            "tags": attributes.get("tags", []),
            "permalink": f"https://www.virustotal.com/gui/ip-address/{ip_Address}"
        }



def check_hash(hash: str) -> dict:
    URL = f"https://www.virustotal.com/api/v3/files/{hash}"

    headers = {
        "accept": "application/json",
        "x-apikey": VIRUS_TOTAL_KEY
    }

    response = requests.get(URL, headers=headers)

    if response.status_code == 404:
        return {
            "Error": f"Error: Hash was not found in the Virus Total database"
        }

    elif response.status_code == 429:
        return {
            "Error": f"Error: Rate limit hit"
        }
    else:
        data = response.json()
        stats = data["data"]["attributes"]["last_analysis_stats"]

        return {
            "hash": hash,
            "malicious": stats["malicious"],
            "suspicious": stats["suspicious"],
            "undetected": stats["undetected"],
            "harmless": stats["harmless"],
            "total_engines": sum(stats.values()),
            "detection_ratio": f"{stats['malicious']}/{sum(stats.values())}",
            "threat_label": data["data"]["attributes"].get("popular_threat_classification", {})
                            .get("suggested_threat_label", "unknown"),
            "permalink": f"https://www.virustotal.com/gui/file/{hash}"
        }