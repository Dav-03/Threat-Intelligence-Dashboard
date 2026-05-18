from deduplication import dup_logic, Write_To_feeds
from OTX_Collector import get_OTX_data
from shodan_enrichment import get_shodan_data
from vt_enrichment import check_hash, check_ip
from apscheduler.schedulers.background import BlockingScheduler
from datetime import datetime 
import time


def main():
    print("Feed collector worker started")
    
    print("fetching OTX data")
    IoC_List = get_OTX_data()
    print(f"Successfullt got {len(IoC_List)} indicators from OTX")

    for IoC in IoC_List:
        print(f"Processing: {IoC['type']} - {IoC["value"]}")
        if IoC["type"].startswith("FileHash"):
            print(f"checking hash with VT")

            Virus_Total_score = check_hash(IoC["value"])
            time.sleep(15)
            if "error" in Virus_Total_score:
                pass
            else:
                IoC["severity"] = Virus_Total_score.get("detection_ratio", IoC["severity"])
            dup_logic(IoC)

        
        elif IoC["type"].startswith("IPv"):
            print(f"Checking IP with VT")
            Virus_Total_score = check_ip(IoC["value"])
            time.sleep(15)
            print(f"Checking IP with Shodan")
            Shodan_report = get_shodan_data(IoC["value"])
            time.sleep(15)
            if "error" in Virus_Total_score:
                pass
            else:
                IoC["severity"] = Virus_Total_score.get("detection_ratio", IoC["severity"])
            dup_logic(IoC)
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

