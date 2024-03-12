import mongo_connect_utils as mc
import redis_connect_utils as rc
import csv
import math 

def main():
    # conn = mc.mongoConnect()
    # conn.startConnection()
    x = 'Arsenal'
    print(math.isnan(x))
    # doc_to_update = {"team": "Arsenal"}
    # update = {"$set" : {"xPts" : 49.39}}

    # result = conn.collection.update_one(doc_to_update, update)
    # conn.initDatabase()
    # with open("raw_data/league_table_14_02_24.csv", encoding='utf-8-sig') as csv_file:
    #         data = csv.reader(csv_file)
    #         test = {}
    #         for row in data:
    #             test[row[1]] = row[len(row) - 1]
    #         print(test)
    # conn = rc.redisConnect()
    # conn.getConnDetails('config/redis_conn.json')
    # conn.startConnection()
    # conn.put({"Arsenal": 47.39})
    
    # ans = conn.get("Arsenal")
    # return ans

if __name__ == "__main__":
    main(); 