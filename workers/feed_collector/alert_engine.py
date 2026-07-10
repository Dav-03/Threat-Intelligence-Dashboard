from database import sessionLocal
from models import Alerts

def run_alert_engine(ioc: dict, iocId: int):
    # takes one IOC and its database id
    # checks it against each rule
    # writes an alert to Postgres if a rule matches
    # skips if an alert already exists for this ioc_id
    db = sessionLocal()
    
    try:
        existing_item = db.query(Alerts).filter(
            Alerts.ioc_id == iocId
        ).first()
        
        if existing_item == None:
            if ioc["type"].startswith("IPv4") and ioc["severity"] == "critical" or ioc["severity"] == "high":
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
            elif ioc["type"].startswith("FileHash") and ioc["severity"] == "critical" or ioc["severity"] == "high":
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
        
        
        
        
        
        

        
        
        
        
#critical_indicator  → severity == "critical"
#high_indicator      → severity == "high"  
#malicious_ip        → type == "IPv4" AND severity in ["high", "critical"]     
        
        
#class Alerts(Base):
#__tablename__ = "alerts"

#ioc_id = Column(Integer, ForeignKey("iocs.id"))
#id = Column(Integer, primary_key = True)
#rule_name = Column(String)
#description = Column(String)
#severity = Column(String)
#timestamp = Column(TIMESTAMP)

#ioc = relationship("IoC", back_populates = "alerts")