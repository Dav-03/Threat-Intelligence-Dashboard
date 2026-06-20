from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class IoC(Base):
    __tablename__ = "iocs"

    id = Column(Integer, primary_key = True)
    type = Column(String)
    value = Column(String)
    source = Column(String)
    severity = Column(String)
    timestamp = Column(TIMESTAMP)


    alerts = relationship("Alerts", back_populates = 'ioc')

#Using Shodan
class Feeds(Base):
    __tablename__ = "feeds"

    ip = Column(String, primary_key = True)
    port = Column(ARRAY(Integer))
    org = Column(String)
    country = Column(String)
    city = Column(String)
    hostname = Column(ARRAY(String))
    data = Column(String)
    timestamp = Column(TIMESTAMP)

class Alerts(Base):
    __tablename__ = "alerts"

    ioc_id = Column(Integer, ForeignKey("iocs.id"))
    id = Column(Integer, primary_key = True)
    rule_name = Column(String)
    description = Column(String)
    severity = Column(String)
    timestamp = Column(TIMESTAMP)

    ioc = relationship("IoC", back_populates = "alerts")

class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key = True)
    username = Column(String, unique = True)
    hashed_password = Column(String)
    email = Column(String)


