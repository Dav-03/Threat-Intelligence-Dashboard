from database import sessionLocal
from models import Alerts

def run_alert_engine(ioc: dict, iocId: int):
    db = sessionLocal()
    
    try:
        existing_item = db.query(Alerts).filter(
            Alerts.ioc_id == iocId
        ).first()
        
        if existing_item == None:
            if ioc["type"].startswith("IPv4") and ioc["severity"] in ["high", "critical"]:
                ruleName = "malicious_ip"
                new_item = Alerts(
                    ioc_id = iocId,
                    rule_name = ruleName,
                    description = f"indicator {ioc['value']} flagged as {ioc['severity']} severity",
                    severity = ioc['severity'],
                    timestamp = ioc['timestamp']
                )
                db.add(new_item)
                db.commit()  
            elif ioc["type"].startswith("FileHash") and ioc["severity"] in ["high", "critical"]:
                ruleName = "malicious_hash"
                new_item = Alerts(
                    ioc_id = iocId,
                    rule_name = ruleName,
                    description = f"indicator {ioc['value']} flagged as {ioc['severity']} severity",
                    severity = ioc['severity'],
                    timestamp = ioc['timestamp']
                )
                db.add(new_item)
                db.commit()  
            else:
                return
        else:
            pass
    
    except:
        db.rollback()
        raise  
    
    finally:
        db.close()
        
