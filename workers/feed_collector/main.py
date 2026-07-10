from deduplication import dup_logic, Write_To_feeds
from alert_engine import run_alert_engine
from OTX_Collector import get_OTX_data
from shodan_enrichment import get_shodan_data
from vt_enrichment import check_hash, check_ip
from apscheduler.schedulers.background import BlockingScheduler
from datetime import datetime 
import time

def score_to_severity(ratio: str) -> str:
    try:
        malicious, total = ratio.split("/")
        ratio = int(malicious) / int(total)
        if ratio == 0:
            return "low"
        elif ratio < 0.1:
            return "medium"
        elif ratio < 0.3:
            return "high"
        else:
            return "critical"
    
    except:
        return "unknown"

def main():
    print("Feed collector worker started")
    
    print("fetching OTX data")
    IoC_List = get_OTX_data()
    print(f"Successfullt got {len(IoC_List)} indicators from OTX")

    for IoC in IoC_List:
        
        print(f"Processing: {IoC['type']} - {IoC['value']}")
        if IoC["type"].startswith("FileHash"):
            print(f"checking hash with VT")

            Virus_Total_score = check_hash(IoC["value"])
            time.sleep(15)
            if "error" in Virus_Total_score:
                pass
            else:
                IoC["severity"] = score_to_severity(Virus_Total_score.get("detection_ratio", "0/1"))
            ioc_db_id = dup_logic(IoC)
            run_alert_engine(IoC, ioc_db_id)

        
        elif IoC["type"].startswith("IPv"):
            Virus_Total_score = check_ip(IoC["value"])
            time.sleep(15)
            Shodan_report = get_shodan_data(IoC["value"])
            time.sleep(15)
            if "error" in Virus_Total_score:
                pass
            else:
                IoC["severity"] = score_to_severity(Virus_Total_score.get("detection_ratio", "0/1"))
            ioc_db_id = dup_logic(IoC)
            run_alert_engine(IoC, ioc_db_id)
            if "error" not in Shodan_report:
                Write_To_feeds(Shodan_report)
        else:
            pass


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'interval', minutes = 15, next_run_time=datetime.now())
    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("Stopping worker")
        scheduler.shutdown()

