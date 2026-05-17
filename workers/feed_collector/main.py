from deduplication import dup_logic, Write_To_feeds
from OTX_Collector import get_OTX_data
from shodan_enrichment import get_shodan_data
from vt_enrichment import check_hash, check_ip
from apscheduler.schedulers.background import BlockingScheduler


def main():
    print("Feed collector worker started")

    IoC_List = get_OTX_data()

    for IoC in IoC_List:
        if IoC["type"].startswith("FileHash"):
            Virus_Total_score = check_hash(IoC["value"])
            if "error" in Virus_Total_score:
                pass
            else:
                IoC["severity"] = Virus_Total_score.get("detection_ratio", IoC["severity"])
            dup_logic(IoC)

        
        elif IoC["type"].startswith("IPv"):
            Virus_Total_score = check_ip(IoC["value"])
            Shodan_report = get_shodan_data(IoC["value"])
            if "error" in Virus_Total_score:
                pass
            else:
                IoC["severity"] = Virus_Total_score.get("detection_ratio", IoC["severity"])
            dup_logic(Shodan_report)
            Write_To_feeds(IoC)

        else:
            pass

scheduler = BlockingScheduler()
scheduler.add_job(main, 'interval', minutes = 15)
scheduler.start()

if __name__ == "__main__":
    main()