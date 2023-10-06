import os
from xata.client import XataClient

#Authenticates Xata.
api_key = os.environ['XATA_API_KEY']

db_url = os.environ['EGW_DB_URL']

xata = XataClient(api_key=api_key, db_url=db_url)

record = xata.records().insert("egw_writings", {
  "content": "“The eyes of all wait upon Thee; And Thou givest them their meat in due season. Thou openest Thine hand, And satisfiest the desire of every living thing.” Psalm 145:15, 16.",
  "book": "Steps to Christ",
  "ref": "SC 9.2",
  "ref_url": "108.23" 
})