from database import sessionLocal
from models import IoC

def dup_logic(item):
    # Writes to Postgres without creating duplicates
    db = sessionLocal()
    
    try:
        existing_item = db.query(IoC).filter(
            IoC.value == item["value"]
        ).first()

        if existing_item == None:
            new_item = IoC(
                type = item["type"],
                value = item["value"],
                source = item["source"],
                severity = item["severity"],
                timestamp = item["timestamp"]
            )

            db.add(new_item)
        
        else:
            existing_item.type = item["type"]
            existing_item.value = item["value"]
            existing_item.source = item["source"]
            existing_item.severity = item["severity"]
            existing_item.timestamp = item["timestamp"]
        db.commit()
    
    except Exception:
        db.rollback()
        raise
    
    finally:
        db.close()