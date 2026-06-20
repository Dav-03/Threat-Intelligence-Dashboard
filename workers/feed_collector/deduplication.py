from database import sessionLocal
from models import IoC, Feeds

def dup_logic(item):
    # Writes to Postgres IoC table without creating duplicates
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



def Write_To_feeds(item):
    # Wrties to Postgres Feeds table without creating duplicates
    db = sessionLocal()

    try:
        existing_item = db.query(Feeds).filter(
            Feeds.ip == item["ip"]
        ).first()

        if existing_item == None:
            new_item = Feeds(
                ip = item["ip"],
                port = item["port"],
                org = item["org"],
                country = item["country"],
                city = item["city"],
                hostname = item["hostname"],
                data = item["data"],
                timestamp = item["timestamp"]
            )
            db.add(new_item)
        
        else:
            existing_item.ip = item["ip"]
            existing_item.port = item["port"]
            existing_item.org = item["org"]
            existing_item.country = item["country"]
            existing_item.city = item["city"]
            existing_item.hostname = item["hostname"]
            existing_item.timestamp = item["timestamp"]
        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()