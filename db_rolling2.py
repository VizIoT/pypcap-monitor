
from pymongo import MongoClient
from config import MONGO_DB_ADDRESS
import time
import logging


IP = 'IP'
TCP = 'TCP'
ETHER = 'Ether'

# writeConcern = pymongo.write_concern.WriteConcern(w=0, wtimeout=None, j=None, fsync=None)
client = MongoClient(MONGO_DB_ADDRESS, serverSelectionTimeoutMS=1)
scapy_database = client['scapy']
tcpAggregatedDataString = 'tcpAggregatedData'
tcp_aggregated_data_collection = scapy_database[tcpAggregatedDataString]

# .with_options(write_concern=writeConcern)

def seven_days_before_milli_time():
  ten_minute_before = time.time() - 60 * 60 * 24 * 7 # seven days before
  return int(round(ten_minute_before * 1000))

'''
Delete the aggregate data seven days ago
'''
def main():
  logging.basicConfig(filename='db_rolling2.log', level=logging.INFO, format='%(asctime)s %(message)s')
  logging.info('Started')
  try:
    time_to_be_deleted = seven_days_before_milli_time()

    # print(list(results))
    # delete data
    result = tcp_aggregated_data_collection.delete_many({
      'endMS': {
        '$lt': time_to_be_deleted
      }
    })
    deleted_count = result.deleted_count

    logging.info('delete entries before ' + str(time_to_be_deleted))
    logging.info('number of records deleted: ' + str(deleted_count))
  except Exception as e:
    print(e)
    logging.error('Error: ' + str(e))
  logging.info('Finished')

if __name__ == '__main__':
  main()