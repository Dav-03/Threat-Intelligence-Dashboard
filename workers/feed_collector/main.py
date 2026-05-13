from deduplication import dup_logic
from OTX_Collector import get_OTX_data
from shodan_enrichment import get_shodan_data
from vt_enrichment import check_hash, check_ip
import os
from dotenv import load_dotenv

load_dotenv()



print("Feed collector worker started")